from traceback import print_tb
from typing import List
from fastapi import Response, status, HTTPException, WebSocket, APIRouter
from broker_manager import BrokerManager
from message_buffer import ConnectionPool, MessageBuffer
import threading

from database_manager import DatabaseManager
from docx import Document
import websockets
import asyncio
import json
import io
from schemas import *


router = APIRouter()

queue_name = 'apiparser'
broker = BrokerManager(queue_name, 'broker')

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


# @router.get("/posts/titles")
# def get_titles(resource: str):
#     queue_name = 'apiparser'
#     broker = BrokerManager(queue_name, 'broker')
#     msg = json.dumps({'type': "titles", 'resource': resource})
#     broker.send_msg(msg)
#     broker.close()
#     return

# websockets
connected_websockets = set()

async def send_message(message):
    if connected_websockets:
        await asyncio.wait([ws.send(message) for ws in connected_websockets])

@router.websocket("/posts/progress/ws")
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

################

# DONE
@router.get("/posts/titles")
async def parse_titles():
    db = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    posts = db.get_all_posts()
    return posts


class ParseTitlesRequest(BaseModel):
    resources: List[str]
    urls: List[str]
    period_days: int

# DONE
@router.post("/posts/titles/test")
async def parse_titles(request: ParseTitlesRequest):
    print('hallo!!!')
    print(request.resources)
    print(request.urls)
    print(request.period_days)

    # buffer = MessageBuffer()
    # connection_pool = ConnectionPool(host="localhost", queue_name="your_queue", buffer=buffer)
    # consumer_thread = threading.Thread(target=connection_pool.consume, args=(consume_callback,))
    # consumer_thread.start()

    # connection_pool.publish(msg)

    parsers = {
        'SCIENTIFICAMERICAN': 'https://www.scientificamerican.com/artificial-intelligence/',
        'MIT': 'https://news.mit.edu/topic/artificial-intelligence2',
        'EXTREMETECH': 'https://www.extremetech.com/tag/artificial-intelligence',
        'VENTUREBEAT': 'https://venturebeat.com/category/ai/',
        'GIZMODO': 'https://gizmodo.com/moderna-ceo-chatgpt-employees-vaccines-openai-1851435620',
        'SYNCED': 'https://syncedreview.com/category/popular/',
    }

    processed_urls = []

    for item in request.resources:
        if item == 'all':
            processed_urls = list(parsers.values())
            break
                
        if item in parsers:
            processed_urls.append(parsers[item])

    for item in request.urls:
        processed_urls.append(item)

    # queue_name = 'apiparser'
    # broker = BrokerManager(queue_name, 'broker')
    msg = json.dumps({'type': 'titles',
                      'resources': processed_urls, 
                      'period_days': request.period_days
                    })
    
    broker.send_msg(msg)
    # broker.close()
    print("отправленно!!!!!!!!")
    return {"message": "Запрос успешно обработан"}


class ProgressRequest(BaseModel):
    current_url_index: str
    url_count: str
    current_article_index: str
    article_count: str

@router.post("/posts/sendprogress")
async def send_progress(request: ProgressRequest):
    print('sended progress')
    print('current_url_index ', request.current_url_index)
    print('url_count ', request.url_count)
    print('current_article_index ', request.current_article_index)
    print('article_count ',  request.article_count)
            # 'current_url_index': current_url_index,
            # 'url_count': url_count,
            # 'current_article_index': current_article_index,
            # 'article_count': article_count,