import pika

class BrokerManager:
    def __init__(self, queue_name: str, host: str):
        self.queue_name = queue_name
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=queue_name)
        except:
            pass

    def set_callback(self, callback):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)

    def send_msg(self, msg):
        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=msg)
        except:
            pass

    def close(self):
        try:
            self.connection.close()
        except:
            pass