import os
import requests


API_URL = os.getenv("API_URL")

class AuthServiceApi: 
    def __init__(self):
        self.session = requests.Session()

    def login_api(self,user: str, password: str):
        response = requests.post(
        url=f"{API_URL}/v1.1/auth",
        json={
            "usuario": user,
            "senha": password
        },
        headers={
            "Content-Type": "application/json"
        }
        )

        response.raise_for_status()

        data = response.json()
        print(data)

        

        return data["response"]["token"]