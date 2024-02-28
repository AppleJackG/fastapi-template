from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from .auth.models import UserAdmin, RefreshTokenAdmin
from .config import settings
from .auth.auth_router import auth_router
from .auth.user_router import user_router
from .auth.superuser_router import superuser_router
from .auth.service import user_service
from .auth.admin import authentication_backend
from .database import engine


app = FastAPI(title="Template")
admin = Admin(app, engine, authentication_backend=authentication_backend)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(superuser_router)

admin.add_view(UserAdmin)
admin.add_view(RefreshTokenAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <a href="http://127.0.0.1:8000/docs">Documentation</a><br>
    <a href="http://127.0.0.1:8000/redoc">ReDoc</a>
    """


@app.get('/protected', dependencies=[Depends(user_service.get_current_user)])
async def protected():
    return {
        'f': 'F'
    }


@app.get('/superprotected', dependencies=[Depends(user_service.get_current_superuser)])
async def superprotected():
    return {
        'f': 'super'
    }
