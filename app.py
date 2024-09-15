from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinjax.catalog import Catalog
from starlette.middleware.sessions import SessionMiddleware

from auth import router as auth_router, authenticate
from config import settings
from database import Session, get_db, init_db
from models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    app.state.sessions = {}
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, tags=["auth"])
app.add_middleware(SessionMiddleware, secret_key=settings.session_key)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include authentication router

# Initialize JinjaX catalog
catalog = Catalog()
catalog.add_folder("templates")


@app.exception_handler(HTTPException)
async def unauthorized_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401 and request.url.path.startswith("/app"):
        return RedirectResponse(url="/")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/", response_class=HTMLResponse)
async def home():
    return catalog.render("Home")


@app.get("/app", response_class=HTMLResponse)
async def dashboard(
    user_id: str = Depends(authenticate), db: Session = Depends(get_db)
):
    user = db.get(User, user_id)
    return catalog.render("Dashboard", user=user)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
