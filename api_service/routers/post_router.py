from typing import Union
from broker_manager import BrokerManager
from pydantic import BaseModel
from database_manager import DatabaseManager
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Response, status, HTTPException
from docx import Document
import json
import io
from fastapi import APIRouter

router = APIRouter()

class Item(BaseModel):
    name: str

class ItemNumber(BaseModel):
    number: int

@router.get("/download/all/")
def download_all_posts():
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
def read_all():
    databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    result = databaseManager.get_all_posts()
    return result


@router.get("/all/del/")
def delete_all():
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


@router.post("/run/")
async def create_item(item: Item):
    queue_name = 'apiparser'
    broker = BrokerManager(queue_name, 'broker')
    msg = json.dumps({'resource': item.name})
    broker.send_msg(msg)
    broker.close()
    return item.name




