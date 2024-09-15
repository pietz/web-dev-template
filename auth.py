import uuid
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from sqlmodel import Session

from config import settings
from models import User
from database import get_db

router = APIRouter()
oauth = OAuth()

if settings.github_client_id and settings.github_client_secret:
    oauth.register(
        name="github",
        client_id=settings.github_client_id,
        client_secret=settings.github_client_secret,
        authorize_url="https://github.com/login/oauth/authorize",
        authorize_params=None,
        access_token_url="https://github.com/login/oauth/access_token",
        access_token_params=None,
        refresh_token_url=None,
        userinfo_endpoint="https://api.github.com/user",
        client_kwargs={"scope": "user:email"},
    )
else:
    print("GitHub OAuth not configured in environment")


def authenticate(request: Request) -> str:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401)
    user_id = request.app.state.sessions.get(session_id)
    if not user_id:
        raise HTTPException(status_code=401)
    return user_id


def get_github_client() -> StarletteOAuth2App:
    github = oauth.create_client("github")
    if not github:
        raise HTTPException(status_code=500)
    return github


@router.get("/github/login")
async def github_login(request: Request):
    github = get_github_client()
    redirect_uri = request.url_for("github_callback")
    return await github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback")
async def github_callback(request: Request, db: Session = Depends(get_db)):
    github = get_github_client()
    token = await github.authorize_access_token(request)
    user_info = await github.userinfo(token=token)
    user = db.get(User, str(user_info["id"]))

    if not user:
        user = User(
            id=str(user_info["id"]),
            login=user_info["login"],
            provider="github",
            name=user_info["name"],
            email=user_info["email"],
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    session_id = str(uuid.uuid4())
    request.app.state.sessions[session_id] = str(user_info["id"])
    response = RedirectResponse(url="/app")
    response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True)
    return response


@router.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    request.app.state.sessions.pop(session_id, None)
    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_id")
    return response
