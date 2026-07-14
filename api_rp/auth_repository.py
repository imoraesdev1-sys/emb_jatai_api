import requests

from api_rp.token_api import TokenApi
from database import SessionLocal
class AuthRepository:

    def __init__(self):
            self.db = SessionLocal()
            self.session = requests.Session()
            self.service_token = TokenApi()

    def close(self):
        """Encerra a sessão do banco."""
        if self.db:
            self.db.close()