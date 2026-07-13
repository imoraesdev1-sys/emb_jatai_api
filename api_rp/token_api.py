from datetime import datetime
import time





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
            
            AuthServiceApi().login_api()
        return self.token

    def _authenticate(self,data):

        self.token = data["response"]["token"]

        self.expires_at = data["response"]["tokenExpiration"]

        print("expiração token", self.expires_at)
        print("Token Salvo com sucesso ..............................................")
        print("_______________________________________________")
        print("Token : ", self.token)