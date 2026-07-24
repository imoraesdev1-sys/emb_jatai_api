from datetime import datetime
import os
import time
from cache_redis.redis_service import RedisService


user=os.getenv("USER")
password=os.getenv("PASSWORD")


class TokenApi:

    def __init__(self):
        self.redis = RedisService()

    def get_token(self):

        from api_rp.auth_service_api import AuthServiceApi
        
        dados = self.redis.get_token()

        print("\n" + "-" * 60)

        if dados:
            ttl = self.redis.client.ttl("rp_api_token")

            print("[TOKEN] Token encontrado no Redis")
            print(f"[TOKEN] TTL restante: {ttl}s")
            print(f"[TOKEN] Expira em: {dados['expires_at']}")

            return dados["token"]

        print("[TOKEN] Token NÃO encontrado")
        print("[TOKEN] Realizando novo login...")

        return AuthServiceApi().login_api(user, password)
    
    def authenticate(self, data):

        print("\n" + "=" * 60)
        print("[AUTH] Iniciando autenticação")

        token = data["response"]["token"]

        expiration = datetime.strptime(
            data["response"]["tokenExpiration"],
            "%d/%m/%Y %H:%M:%S"
        )

        ttl = data["response"]["expiresIn"]

        print(f"[AUTH] Token: {token[:30]}...")
        print(f"[AUTH] Expiração API: {expiration}")
        print(f"[AUTH] TTL recebido: {ttl}s")

        self.redis.save_token(
            token=token,
            expires_at=expiration,
            ttl=ttl
        )

        ttl_redis = self.redis.client.ttl("rp_api_token")
        dados_redis = self.redis.get_token()

        print("[AUTH] Token salvo no Redis")
        print(f"[AUTH] TTL Redis: {ttl_redis}s")
        print(f"[AUTH] Redis: {dados_redis}")
        print("=" * 60 + "\n")
