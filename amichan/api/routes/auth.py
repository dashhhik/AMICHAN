import re
from datetime import timedelta
from fastapi import APIRouter, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from amichan.api.schemas.requests.auth import BanUserRequest
from amichan.core.config import DevAppSettings
from pydantic import BaseModel, EmailStr

from amichan.core.dependencies import IJWTService, CurrentUser

router = APIRouter()

settings = DevAppSettings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_FROM_NAME="AMICHAN",
)
VALID_EMAIL_REGEX = r".+@edu\.hse\.ru$"


class EmailSchema(BaseModel):
    email: EmailStr


@router.post("/send_magic_link/")
async def send_magic_link(email_data: EmailSchema, jwt_service: IJWTService):
    email = email_data.email

    if not re.match(VALID_EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Invalid email domain")

    try:
        token = await jwt_service.generate(email, 1, timedelta(minutes=5))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create token: {str(e)}")

    magic_link = f"http://localhost:8000/auth/verify_magic_link/{token}"

    message = MessageSchema(
        subject="Your Magic Link",
        recipients=[email],
        body=f"Click the link to log in: {magic_link}",
        subtype="plain",
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    return {"message": f"Magic link sent to {email}"}


@router.get("/verify_magic_link/{token}")
async def verify_magic_link(token: str, jwt_service: IJWTService):
    try:
        user = await jwt_service.parse(token)
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        new_token = await jwt_service.generate(
            user.email, user.role_id, timedelta(days=30)
        )
        return {"token": new_token}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Token verification failed: {str(e)}"
        )


@router.post("/ban_user/")
async def ban_user(
    current_user: CurrentUser, ban_data: BanUserRequest, jwt_service: IJWTService
):
    email = ban_data.email

    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if current_user.role_id > 2:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not re.match(VALID_EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Invalid email domain")

    await jwt_service.ban_user(email, ban_data.reason, ban_data.duration)

    message = MessageSchema(
        subject="You have been banned",
        recipients=[email],
        body=f"Your account has been banned. If you believe this is a mistake, contact the administrators.",
        subtype="plain",
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    return {"message": f"User {email} has been banned"}
