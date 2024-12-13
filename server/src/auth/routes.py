from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# from fastapi.security import HTTPAuthorizationCredenials
from .models import User, UserBase, UserLogin
from .services import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token, verify_password
from datetime import timedelta
from src.config import Config

auth_router = APIRouter()
user_service = UserService()
# refresh = RefreshTokenBearer()
# role = Depends(RoleCheker(["admin"]))


@auth_router.post("/signup", response_model=User, status_code=200)
async def create_user_account(
    user: UserBase, session: AsyncSession = Depends(get_session)
):
    email = user.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=403, detail=f"User with email: {email} already exists"
        )
    new_user = await user_service.create(user, session)
    return new_user


@auth_router.post("/login")
async def login(credentials: UserLogin, session: AsyncSession = Depends(get_session)):
    email = credentials.email
    password = credentials.password
    user = await user_service.retrieve_by_email(email, session)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with email: {email} not found"
        )
    password_valid = verify_password(password, user.password)

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials. Please check your password.",
        )

    access_token = create_access_token(
        user_data={
            "username": user.username,
            "email": user.email,
            "role": user.role,
        },
    )

    refresh_token = create_access_token(
        user_data={
            "username": user.username,
            "email": user.email,
            "role": user.role,
        },
        refresh=True,
        exp=timedelta(days=Config.REFRESH_TOKEN_EXP),
    )

    return JSONResponse(
        content={
            "msg": "Login Sucessful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"id": str(user.id), "email": user.email},
        },
        status_code=200,
    )


# @auth_router.get("/refresh_token")
# async def create_new_access_token(
#     credentials: HTTPAuthorizationCredentials = Depends(refresh),
# ):
#     exp_date = credentials["exp"]
#     if not (datetime.fromtimestamp(exp_date) > datetime.now()):
#         raise HTTPException(
#             status_code=400, detail="Refresh token expired. Please log in again."
#         )

#     new_access_token = create_access_token(user_data=credentials["user"])
#     return JSONResponse(content={"access_token": new_access_token})


# @auth_router.get("/me", dependencies=[role])
# async def get_details(user=Depends(get_curr_user), session=Depends(get_session)):
#     return {"user": user}


# @auth_router.get("/logout")
# async def revoke_token(
#     credentials: HTTPAuthorizationCredentials = Depends(refresh),
# ):
#     await blacklist_token(credentials["jti"])

#     return JSONResponse(
#         content={"msg": "Token revoked. Logout sucess"}, status_code=200
#     )
