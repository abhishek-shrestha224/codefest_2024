from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from uuid import uuid4
from src.config import Config
from jwt.exceptions import ExpiredSignatureError, ImmatureSignatureError, PyJWTError


password_context = CryptContext(schemes=["bcrypt"])


def generate_hash(password: str):
    hash = password_context.hash(password)
    return hash


def verify_password(password: str, hash: str):
    return password_context.verify(password, hash)


def create_access_token(
    user_data: dict, refresh: bool = False, exp: timedelta = None
) -> str:
    payload = {
        "user": user_data,
        "iat": int(datetime.now().timestamp()),
        "exp": int(
            (
                datetime.now()
                + (exp if exp else timedelta(seconds=Config.ACCESS_TOKEN_EXP))
            ).timestamp()
        ),
        "jti": str(uuid4()),
        "refresh": refresh,
    }
    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGO
    )
    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGO]
        )
        return token_data

    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Your token has expired")

    except ImmatureSignatureError:
        raise HTTPException(status_code=400, detail="Your token has not matured yet.")

    except PyJWTError:
        raise HTTPException(status_code=400, detail="This token is invalid or expired")
