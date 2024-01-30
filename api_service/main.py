from typing import Union
from broker_manager import BrokerManager

from fastapi import FastAPI

app = FastAPI()

# start parsing
# get post from article
# get articles

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/run/")
async def create_item():
    queue_name = 'apiparser'
    broker = BrokerManager(queue_name, 'broker')
    msg = 'send'
    broker.send_msg(msg)
    broker.close()
    return "super"