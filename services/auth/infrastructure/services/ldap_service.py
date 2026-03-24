import ldap3
from ldap3 import Server, Connection, ALL
from config.settings import settings
from typing import Optional, Dict

class LDAPService:
    """LDAP认证服务"""
    
    def __init__(self):
        self.server = Server(settings.ldap_url, get_info=ALL)
        self.base_dn = settings.ldap_base
        self.user_prefix = settings.ldap_user_prefix
    
    async def authenticate(self, email: str, password: str) -> Optional[Dict]:
        """
        LDAP认证用户
        :param email: 用户邮箱
        :param password: 用户密码
        :return: 用户信息，认证失败返回None
        """
        try:
            # 提取邮箱前缀作为账号
            account = email.split('@')[0]
            
            # 构造LDAP用户名
            ldap_user = f"{self.user_prefix}{account}"
            
            # 建立连接
            conn = Connection(
                self.server,
                user=ldap_user,
                password=password,
                auto_bind=False,
                read_only=True
            )
            
            if not conn.bind():
                conn.unbind()
                return None
            
            # 查询用户信息
            search_filter = f"(userPrincipalName={email})"
            conn.search(
                search_base=self.base_dn,
                search_filter=search_filter,
                search_scope=ldap3.SUBTREE,
                attributes=['cn', 'sAMAccountName', 'mail', 'displayName']
            )
            
            if not conn.entries:
                conn.unbind()
                return None
            
            user_entry = conn.entries[0]
            user_info = {
                'account': str(user_entry.sAMAccountName),
                'email': str(user_entry.mail) if hasattr(user_entry, 'mail') else email,
                'username': str(user_entry.displayName) if hasattr(user_entry, 'displayName') else str(user_entry.cn)
            }
            
            conn.unbind()
            return user_info
            
        except Exception as e:
            print(f"LDAP认证错误: {str(e)}")
            return None

# 全局LDAP服务实例
ldap_service = LDAPService()