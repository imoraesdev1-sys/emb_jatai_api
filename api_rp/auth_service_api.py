
import os
from fastapi import HTTPException
import requests
from sqlalchemy.orm import Session
from api_rp.token_api import TokenApi
from sqlalchemy import select, func

from product.product_model import Products




API_URL = os.getenv("API_URL")

class AuthServiceApi: 

    service_token= TokenApi()

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

        self.service_token._authenticate(data)

        return data["response"]["token"]
    

    def get_product(self, db: Session, code: int | None = None):

        if code is None:
            menor_codigo = db.execute(
                select(func.min(Products.codigo))
            ).scalar_one()
        else:
            menor_codigo = code

        response = requests.get(
            url=f"{API_URL}/v1.1/produto/listaprodutos/{menor_codigo}",
            headers={
                "Content-Type": "application/json",
                "token": self.service_token.token
            }
        )

        # response.raise_for_status()
        data=response.json()

        
        if "error" in data:
            raise HTTPException(
                status_code=401,
                detail=data["error"]
            )

        return data["produtos"]






    def compare_products(self, db: Session):

        ultimo_codigo = 0  
        produtos_inseridos = []

        try:
            while True:
                if ultimo_codigo == 0: 
                    produtos = self.get_product(db)
                
                produtos = self.get_product(db, ultimo_codigo)

                

                if not produtos:
                    break

                for item in produtos:

                    produto = db.execute(
                        select(Products).where(
                            Products.codigo == item["codigo"]
                        )
                    ).scalar_one_or_none()

                    if produto is None:

                        produto = Products(
                            codigo=item["codigo"],
                            descricao=item["descricao"],
                            unidade=item["embalagem"],
                            marca=item["marca"],
                            codigo_grupo=int(item["grupoCodigo"])
                        )

                        db.add(produto)
                        produtos_inseridos.append(produto)

                db.commit()

         
                ultimo_codigo = produtos[-1]["codigo"]
                print("ultimo codigo : ",ultimo_codigo)

          
                if len(produtos) < 100:
                    break

            for produto in produtos_inseridos:
                db.refresh(produto)

            return produtos_inseridos

        except Exception:
            db.rollback()
            raise
    
        
 



    """ 
        Codigo existe na base ? 
        Atualiza banco de dados
        Codigo não existe? 
        Insert banco de dados

    """
            

