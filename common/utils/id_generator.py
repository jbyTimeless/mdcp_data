import time
import secrets
import string
import base64
from typing import Optional
from config.settings import settings

class SnowflakeGenerator:
    """雪花算法ID生成器"""
    # 起始时间戳 (2024-01-01 00:00:00)
    EPOCH = 1704067200000
    
    # 各部分位数
    WORKER_ID_BITS = 5
    DATACENTER_ID_BITS = 5
    SEQUENCE_BITS = 12
    
    # 最大值
    MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
    MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)
    
    # 移位
    WORKER_ID_SHIFT = SEQUENCE_BITS
    DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS
    
    # 序列号掩码
    SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)
    
    def __init__(self, worker_id: int = 1, datacenter_id: int = 1):
        if worker_id > self.MAX_WORKER_ID or worker_id < 0:
            raise ValueError(f"Worker ID must be between 0 and {self.MAX_WORKER_ID}")
        if datacenter_id > self.MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError(f"Datacenter ID must be between 0 and {self.MAX_DATACENTER_ID}")
            
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = 0
        self.last_timestamp = -1
    
    def _get_current_timestamp(self) -> int:
        return int(time.time() * 1000)
    
    def _wait_next_millis(self, last_timestamp: int) -> int:
        timestamp = self._get_current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_current_timestamp()
        return timestamp
    
    def generate_id(self) -> int:
        timestamp = self._get_current_timestamp()
        
        if timestamp < self.last_timestamp:
            raise RuntimeError("Clock moved backwards. Refusing to generate id")
        
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._wait_next_millis(self.last_timestamp)
        else:
            self.sequence = 0
        
        self.last_timestamp = timestamp
        
        return ((timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT) | \
               (self.datacenter_id << self.DATACENTER_ID_SHIFT) | \
               (self.worker_id << self.WORKER_ID_SHIFT) | \
               self.sequence

# 全局ID生成器实例
snowflake = SnowflakeGenerator(
    worker_id=settings.snowflake_worker_id,
    datacenter_id=settings.snowflake_datacenter_id
)

# Base62字符集
BASE62_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits

def generate_user_id() -> str:
    """生成用户ID（雪花算法）"""
    return str(snowflake.generate_id())

def generate_access_key(prefix: str = "MDCP_AK_", length: int = 32) -> str:
    """生成Access Key（高熵随机字符串）"""
    random_part = ''.join(secrets.choice(BASE62_CHARS) for _ in range(length))
    return f"{prefix}{random_part}"

def generate_secret_key(byte_length: int = 32) -> str:
    """生成Secret Key（密码学安全随机数，Base64编码）"""
    random_bytes = secrets.token_bytes(byte_length)
    return base64.b64encode(random_bytes).decode('utf-8')