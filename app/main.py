from fastapi import FastAPI
from routers import authentication
from routers import ecg
from routers import user

app = FastAPI()

app.include_router(authentication.router)
app.include_router(ecg.router)
app.include_router(user.router)
