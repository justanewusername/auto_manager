from turtle import pos
from broker_manager import BrokerManager
from gpt_manager import GPTManager
from database_manager import DatabaseManager
import json
import time
import requests
from request_manager import send_post


def callback(ch, method, properties, body):
    print("callback started")
    msg = json.loads(body)
    print('msg: ', msg)
    gpt = GPTManager()
    post = ""
    try:
        post = gpt.get_post(msg['content'])
    except:
        print('oh no!')
        return
    if len(post) < 100:
        print('oh no!')
        return
    print('sending post...')
    send_post(msg['user_id'], post)
    # send_post(msg['user_id'], msg['content'])
    print('done')
    
    # db_manager = DatabaseManager('postgresql://user:qwerty@db:5432/mydbname')
    # db_manager.create_post(post, msg['title'], msg['url'], msg['category'], msg['resource'])
    # print('post saved.')


queue_name = 'articles'
broker = BrokerManager(queue_name, 'broker')
broker.set_callback(callback)


print(' [*] Waiting for messages.')
broker.start_consuming()