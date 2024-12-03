import secrets

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import Response

from amichan.core.dependencies import IOAuthService

router = APIRouter()

CLIENT_ID = "b5f53593e3f54c1880be87db24c73fb2"
REDIRECT_URI = "https://oauth.yandex.ru/verification_code"
AUTH_URL = "https://oauth.yandex.ru/authorize"



@router.get("/")
async def redirect_to_oauth(response: Response):
    state = secrets.token_urlsafe(16)
    response.set_cookie(key="oauth_state", value=state, httponly=True, secure=True)
    oauth_url = (
        f"{AUTH_URL}"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=login:email"
        f"&state={state}"
    )
    return RedirectResponse(oauth_url)


@router.get("/callback")
async def oauth_callback(
    request: Request, yandexOauthService: IOAuthService, response: Response
):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    oauth_state = request.cookies.get("oauth_state")

    if not code:
        raise HTTPException(status_code=400, detail="Authorization code is missing")
    if state != oauth_state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    email, access_token = await yandexOauthService.callback(request)

    if not email or not email.endswith("@edu.hse.ru"):
        raise HTTPException(
            status_code=403,
            detail="Email must belong to @edu.hse.ru domain",
        )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Ограничивает доступ к cookie из JavaScript
        secure=True,  # Только для HTTPS
        max_age=3600,  # Срок действия токена
    )

    return RedirectResponse(url="/")
