from sqlalchemy.orm import Session
from product_model import Products

from sqlalchemy import text
class ProductRepository:
    def __init__(self, db:Session):
        self.db=db


    def get_by_id(self, product_id: int):
        return self.db.query(Products).filter(
            Products.id == product_id
        ).first()