from turtle import pos
from broker_manager import BrokerManager
from gpt_manager import GPTManager
from database_manager import DatabaseManager
import json
import time


def callback(ch, method, properties, body):
    time.sleep(20)
    msg = json.loads(body)
    gpt = GPTManager()
    post = ""
    try:
        post = gpt.get_post(msg['content'])
    except:
        return
    if len(post) < 100:
        return

    db_manager = DatabaseManager('postgresql://user:qwerty@db:5432/mydbname')
    db_manager.create_post(post, msg['title'], msg['url'], msg['category'], msg['resource'])
    print('post saved.')


queue_name = 'articles'
broker = BrokerManager(queue_name, 'broker')
broker.set_callback(callback)


print(' [*] Waiting for messages.')
broker.channel.start_consuming()
