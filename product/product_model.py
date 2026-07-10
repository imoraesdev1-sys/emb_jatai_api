
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Float, Integer, String

from database import Base


class ProductsBaseModel(BaseModel):

    id:int 
    code:int
    description:str 
    ativo:bool


class Products(Base):
    __tablename__ = "produto"
    __table_args__ = {"schema": "embjatai"}

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(Integer, nullable=False)
    descricao = Column(String, nullable=False)
    ativo= Column(Boolean, default=True )
    valor=Column(Float)
    unidade=Column(String)