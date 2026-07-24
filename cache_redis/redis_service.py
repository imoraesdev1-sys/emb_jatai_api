import redis
import json
from datetime import datetime
class RedisService:

    def __init__(self):
        self.client = redis.Redis(
            host="painel.devia.store",
            port=6379,
            username="default",
            password="Ricardo@0511",
            decode_responses=True
        )



    def get_token(self):
        data = self.client.get("rp_api_token")

        if not data:
            return None

        return json.loads(data)


    def save_token(self, token: str, expires_at: datetime, ttl: int):

        self.client.setex(
            "rp_api_token",
            ttl,
            json.dumps({
                "token": token,
                "expires_at": expires_at.strftime("%d/%m/%Y %H:%M:%S")
            })
        )