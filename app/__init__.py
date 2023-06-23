from fastapi import FastAPI
from app.api import voices, locales

app = FastAPI()

app.include_router(voices.router)
app.include_router(locales.router)