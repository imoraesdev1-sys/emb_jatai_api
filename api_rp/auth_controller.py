

from fastapi import APIRouter

from api_rp.auth_model import AuthModel
from api_rp.auth_service_api import AuthServiceApi

service=AuthServiceApi()
router=APIRouter(
    prefix='/rp_api',
    tags=["RP API"]
)


@router.post("/auth")
def auth_login(login:AuthModel):
    
    return service.login_api(login.user, login.password)


@router.get("/products/list_products")
def list_products(code: int | None = None):
    return service.get_product(code)
    
