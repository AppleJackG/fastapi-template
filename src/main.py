from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .auth.router import auth_router, user_router
from .auth.service import user_service

app = FastAPI(title="Template")

app.include_router(auth_router)
app.include_router(user_router)

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