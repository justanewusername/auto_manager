from typing import Union
from broker_manager import BrokerManager
from pydantic import BaseModel
from database_manager import DatabaseManager
from fastapi.middleware.cors import CORSMiddleware

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

# get post from article
# get articles

class Item(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/all/")
def read_all():
    databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    result = databaseManager.get_all_posts()
    return result

@app.get("/all/del/")
def delete_all():
    databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    result = databaseManager.delete_all_posts()
    return result

@app.post("/del/")
async def create_item(item: Item):
    databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    result = databaseManager.delete_post_by_identifier(item.name)
    return result

@app.post("/run/")
async def create_item(item: Item):
    queue_name = 'apiparser'
    broker = BrokerManager(queue_name, 'broker')
    msg = item.name # all, Scientificamerican, MIT, Extremetech
    broker.send_msg(msg)
    broker.close()
    return 'wow'
