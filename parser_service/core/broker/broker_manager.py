import pika
import time

class BrokerManager:
    def __init__(self, queue_name: str, host: str):
        self.queue_name = queue_name
        self.host = host
        self.connect_to_broker()


    def connect_to_broker(self):
        while True:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.queue_name)
                break
            except pika.exceptions.AMQPConnectionError as e:
                print(f"Connection error: {e}. Retrying in 5 seconds...")
                time.sleep(5)


    def set_callback(self, callback):
        self.callback = callback
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self._wrapped_callback, auto_ack=True)


    def _wrapped_callback(self, ch, method, properties, body):
        try:
            self.callback(ch, method, properties, body)
        except pika.exceptions.AMQPConnectionError:
            print("Connection lost. Reconnecting...")
            self.connect_to_broker()
            self.set_callback(self.callback)


    def send_msg(self, msg):
        while True:
            try:
                self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=msg)
                break
            except pika.exceptions.AMQPConnectionError as e:
                print(f"Connection error while sending message: {e}. Reconnecting...")
                self.connect_to_broker()


    def close(self):
        self.connection.close()
