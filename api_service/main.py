import os

os.environ['JWT_SECRET_KEY'] = '48d6926cfa170d8a387752116262bc83016e6e5da1ce98d29c205cb24746344c'
os.environ['JWT_REFRESH_SECRET_KEY'] = '9bf39ebb7068cc079678a6f17cfdf65d9c657dc09133c2a4bb78f9f2aa03f2d4'

from fastapi.middleware.cors import CORSMiddleware
from routers import favorites_router, post_router, auth_router
from fastapi import FastAPI


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(favorites_router.router)
app.include_router(post_router.router)
app.include_router(auth_router.router)
