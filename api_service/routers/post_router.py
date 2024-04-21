from fastapi import Response, status, HTTPException, WebSocket, APIRouter
from broker_manager import BrokerManager
from pydantic import BaseModel

from database_manager import DatabaseManager
from docx import Document
import websockets
import asyncio
import json
import io


router = APIRouter()

class Item(BaseModel):
    name: str

class ItemNumber(BaseModel):
    number: int

@router.get("/download/all/")
async def download_all_posts():
    try:
        # Преобразование данных в .doc
        doc = Document()
        doc.add_heading('Сгенерированные посты', level=1)

        databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
        posts = databaseManager.get_all_posts()
        for post in posts:
            doc.add_heading(post['title'], level=2)
            doc.add_paragraph(post['article'])
            doc.add_paragraph(post['url'])
            doc.add_paragraph('')
            doc.add_paragraph('')
        
        # Создание байтового потока для хранения .doc файла
        doc_stream = io.BytesIO()
        doc.save(doc_stream)
        doc_stream.seek(0)
        
        # Отправка файла в ответе
        return Response(doc_stream.getvalue(), media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', headers={"Content-Disposition": "attachment;filename=posts.docx"})
    except Exception as e:
        print(f"Error generating or sending .doc file: {e}")
        return Response(status_code=500)


@router.get("/all/")
async def read_all():
    databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    result = databaseManager.get_all_posts()
    return result


@router.get("/all/del/")
async def delete_all():
    databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    result = databaseManager.delete_all_posts()
    return result


@router.post("/del/")
async def delete_item(item: ItemNumber):
    databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    result = databaseManager.delete_post_by_id(item.number)
    return result


@router.post("/create/")
async def create_item(item: Item):
    databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    result = databaseManager.create_post(item.name)
    return result


@router.post("/run")
async def create_item(item: Item):
    queue_name = 'apiparser'
    broker = BrokerManager(queue_name, 'broker')
    msg = json.dumps({'type': 'standart','resource': item.name})
    broker.send_msg(msg)
    broker.close()
    return item.name


@router.get("/posts/titles")
def get_titles(resource: str):
    queue_name = 'apiparser'
    broker = BrokerManager(queue_name, 'broker')
    msg = json.dumps({'type': "titles", 'resource': resource})
    broker.send_msg(msg)
    broker.close()
    return

@router.post("/posts/titles")
async def set_titles(titles: list):
    send_message(titles)
    return

# websockets
connected_websockets = set()

async def send_message(message):
    if connected_websockets:
        await asyncio.wait([ws.send(message) for ws in connected_websockets])

@router.websocket("/posts/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    print(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await send_message(data)
    except websockets.exceptions.ConnectionClosedError:
        connected_websockets.remove(websocket)