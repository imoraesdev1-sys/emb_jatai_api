from datetime import datetime
import os
import time


user=os.getenv("USER")
password=os.getenv("PASSWORD")


class TokenApi:   

   

    def __init__(self):
        self.token = None
        self.expires_at = None

    def get_token(self):

        from api_rp.auth_service_api import AuthServiceApi

        if (
            self.token is None
            or self.expires_at is None
            or datetime.now() >= self.expires_at
        ):
            
            AuthServiceApi().login_api(user, password)

        return self.token

    def _authenticate(self,data):

        self.token = data["response"]["token"]

        self.expires_at = datetime.strptime(
        data["response"]["tokenExpiration"],
        "%d/%m/%Y %H:%M:%S"
        )

