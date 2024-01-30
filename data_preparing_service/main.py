from broker_manager import BrokerManager
from gpt_manager import GPTManager
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

    # send post
    queue = msg['destination'] #'posts'
    br = BrokerManager(queue, 'broker')
    msg = json.dumps({'content': post, 'url': msg['url']})
    # br.channel.basic_publish(exchange='', routing_key=queue, body=msg)
    br.send_msg(msg)
    br.close()


queue_name = 'articles'
broker = BrokerManager(queue_name, 'broker')
broker.set_callback(callback)


print(' [*] Waiting for messages.')
broker.channel.start_consuming()
