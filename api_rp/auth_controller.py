

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from api_rp.auth_repository import AuthRepository
from database import get_db

from api_rp.auth_model import AuthModel
from api_rp.auth_service_api import AuthServiceApi


router=APIRouter(
    prefix='/rp_api',
    tags=["RP API"]
)


@router.post("/auth")
def auth_login(login:AuthModel):
    service = AuthServiceApi()
    return service.login_api(login.user, login.password)


@router.get("/products/list_products")
def list_products(
    code: int | None = None,
    db: Session = Depends(get_db)
):
    service = AuthServiceApi()
    return service.get_product(db, code)


@router.post("/close-session")
def close_session():
    service = AuthRepository()

    try:
        service.close()
        return {
            "success": True,
            "message": "Sessão encerrada com sucesso."
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

@router.get("/products/compare")
def compare_products(
db: Session = Depends(get_db)
):
    service = AuthServiceApi()
    return service.compare_products(db)


@router.get("/product/price")
def price_product(
    code, 
    db:Session=Depends(get_db)): 
    service= AuthServiceApi()
    return service.price_product(code,db)
