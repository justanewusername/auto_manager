from typing import Union
from broker_manager import BrokerManager
from pydantic import BaseModel
from database_manager import DatabaseManager
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Response
from docx import Document
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

databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")

# get post from article
# get articles

class Item(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/download/all/")
def download_all_posts():
    try:
        # Преобразование данных в .doc
        doc = Document()
        doc.add_heading('Сгенерированные посты', level=1)

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


@app.get("/all/")
def read_all():
    result = databaseManager.get_all_posts()
    return result

@app.get("/all/del/")
def delete_all():
    result = databaseManager.delete_all_posts()
    return result

@app.post("/del/")
async def create_item(item: Item):
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
