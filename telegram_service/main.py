from bestconfig import Config
import asyncio
from core.broker import BrokerManager
import logging
import aiogram
import time
import threading
import json
from aiogram import Bot, Dispatcher, types, executor
import pika
from asyncio import new_event_loop, set_event_loop
from core.database_manager import DatabaseManager

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# Настройки телеграм-бота
config = Config()
API_TOKEN = str(config['API_TOKEN'])
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# connect DB
db_manager = DatabaseManager(config['DB_STRING'])


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    print(message['chat']['id'])
    db_manager.create_chat(message['chat']['id'])
    await message.answer("Привет! Скоро я отправлю тебе посты со свежими новостями")


async def process_answers(self, message: types.Message):
    print(type(message))
    if 'reply_to_message' in message:
        if 'text' in message['reply_to_message']:
            print(message['reply_to_message']['text'])
            if db_manager.get_post_by_article(message['reply_to_message']['text'] is not None):
                print("тут сохранили")
                await message.answer("Спасибо за ответ!")
            else:
                await message.answer("Пост не найден. Возможно вы ответили не на то сообщение")
                
    else:
        await message.answer("Вы должны написать ответ к одному из сообщений")

async def callback(ch, method, properties, body):
    print("wow")
    msg = json.loads(body)
    post = msg['content']
    print(post)
    db_manager.create_post(post)

    # users = await bot.get_chat_members(chat_id='@ru_recipes_bot', limit=100)  # Замените на свой канал
    users = db_manager.get_all_chat_id()
    for user in users:
        user_id = user.user.id
        # Отправка сообщения каждому пользователю
        await bot.send_message(chat_id=user_id, text=post)


def start_polling_rabbitmq():
    queue_name = config['QUEUE_NAME']
    print('queue_name::: ', queue_name)
    broker = BrokerManager(queue_name, 'broker')
    broker.set_callback(callback)
    broker.channel.start_consuming()

# def on_startup(dp):
#     task = asyncio.create_task(start_polling_rabbitmq())

def start_telegram():
    set_event_loop(new_event_loop())
    executor.start_polling(dp)

dp.register_message_handler(process_answers)
print("tttt")

print("hera")
# Запуск асинхронного прослушивания сообщений из RabbitMQ
thread1 = threading.Thread(target=start_telegram)
thread1.start()
thread1.join()

# thread2 = threading.Thread(target=start_polling_rabbitmq)
# thread2.start()
# thread2.join()
