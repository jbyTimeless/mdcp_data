from elasticsearch import AsyncElasticsearch
from config.settings import settings

def get_es_client() -> AsyncElasticsearch:
    # 移除所有手动headers、meta_header，仅保留核心配置
    return AsyncElasticsearch(
        hosts=[settings.es_host],  # 标准写法，兼容http://ip:port
    )

es_client = get_es_client()