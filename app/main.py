from fastapi import FastAPI
from .db import Base, engine
from . import models  
from .routers.auth import router as auth_router
from .routers.pois import router as pois_router

app = FastAPI(title="Louisiana Routes API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def health():
    return {"status": "ok"}

app.include_router(pois_router)
