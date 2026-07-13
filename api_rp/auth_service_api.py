import os
import requests

from api_rp.token_api import TokenApi
from sqlalchemy import select, func

from product.product_model import Products
from database import SessionLocal

db = SessionLocal()

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
    

    def get_product(self, code: int | None = None):
        """
        O intuito é buscar o menor numero possivel para puxar na api a listagem de produtos.
        """
        if code == None:
            menor_codigo =db.execute(
            select(func.min(Products.codigo))
            ).scalar_one()
            print(menor_codigo)
        else:
            menor_codigo=code
        
        # traz 100 produtos.

        response = requests.get(
        url=f"{API_URL}/v1.1/produto/listaprodutos/{menor_codigo}",
        headers={
            "Content-Type": "application/json", 
            "token":self.service_token.token
        }
        )
        data=response.json()
        data=data["produtos"]

        return data




    def compare_products(self,produtos):

        for item in produtos:

            stmt = select(Products).where(Products.codigo == item.codigo)

            produto = db.execute(stmt).scalar_one_or_none()

            if produto is None:
                produto = Products(
                    codigo=item.codigo,
                    descricao=item.descricao,
                    valor=item.valor,
                    unidade=item.unidade
                )

                db.add(produto)
                db.commit()
                db.refresh(produto)

        return produto
    
        
    """
    Select no banco interno com lista de codigos trazidos da api do RP, conferir informações banco e da api. 
    lista_produtos_api=[]
    lista_produtos_db=[]
    """



    """ 
        Codigo existe na base ? 
        Atualiza banco de dados
        Codigo não existe? 
        Insert banco de dados

    """
            

