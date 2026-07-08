from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from product_repository import ProductRepository
from product_service import ProductService


router= APIRouter(
   prefix='/product',
   tags=["products"]
)


@router.get("/get_by_id/{product_id}")
def get_product_by_id(product_id:int,db: Session = Depends(get_db)):
   repository=ProductRepository(db)
   service=ProductService(repository)
   return service.get_product_id(product_id)

@router.get("/get_product_active")
def get_product_active(db: Session = Depends(get_db)):
   repository=ProductRepository(db)
   service=ProductService(repository)
   return service.get_product_active()


@router.get("/get_description_product/{description}")
def get_description_product(description:str,db: Session = Depends(get_db)):
   repository=ProductRepository(db)
   service=ProductService(repository)
   return service.get_description_product(description)