

from fastapi import APIRouter

from api_rp.auth_service_api import AuthServiceApi


router=APIRouter(
    prefix='/rp_api',
    tags=["RP API"]
)


@router.get("/auth/{user}/{password}")
def auth_login(user:str,password:str):
    service=AuthServiceApi()
    return service.login_api(user, password)

