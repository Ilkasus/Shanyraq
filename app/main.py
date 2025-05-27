from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.auth.routes import auth_router
from app.shanyraks.routes import shanyrak_router
from app.comments.routes import comment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Şañyraq.kz",
    description="Полноценная платформа объявлений о недвижимости",
    version="1.0.0"
)

# CORS (если фронтенд будет на React/Vue)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(auth_router, prefix="/auth")
app.include_router(shanyrak_router, prefix="/shanyraks")
app.include_router(comment_router, prefix="/comments")

