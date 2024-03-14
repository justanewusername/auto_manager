import pika

class BrokerManager:
    def __init__(self, queue_name: str, host: str):
        self.queue_name = queue_name

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def set_callback(self, callback):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
