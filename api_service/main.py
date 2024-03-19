from typing import Union
from broker_manager import BrokerManager
from pydantic import BaseModel
from database_manager import DatabaseManager
from fastapi.middleware.cors import CORSMiddleware
from routers import favorites_router, post_router

from fastapi import FastAPI, Response, status, HTTPException
from docx import Document
import json
import io

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