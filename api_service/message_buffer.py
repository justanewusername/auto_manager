import pika
import queue


class MessageBuffer:
    def __init__(self):
        self._buffer = queue.Queue()

    def put(self, msg):
        self._buffer.put(msg)

    def get(self):
        return self._buffer.get()

class ConnectionPool:
    def __init__(self, host, queue_name, buffer, pool_size=5):
        self.host = host
        self.queue_name = queue_name
        self.buffer = buffer
        self.pool = [self._create_connection() for _ in range(pool_size)]

    def _create_connection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        return connection, channel

    def publish(self, msg):
        connection, channel = self.pool.pop(0)
        try:
            channel.basic_publish(exchange='', routing_key=self.queue_name, body=msg)
        except:
            pass
        self.pool.append(self._create_connection())
        self.buffer.put(msg)

    def consume(self, callback):
        while True:
            msg = self.buffer.get()
            callback(msg)

