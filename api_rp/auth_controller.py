

from fastapi import APIRouter

from api_rp.auth_model import AuthModel
from api_rp.auth_service_api import AuthServiceApi


router=APIRouter(
    prefix='/rp_api',
    tags=["RP API"]
)


@router.post("/auth")
def auth_login(login:AuthModel):
    service=AuthServiceApi()
    return service.login_api(login.user, login.password)

