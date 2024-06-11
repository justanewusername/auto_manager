from bestconfig import Config
from core.parsers import MultiParser
from scrapy import cmdline
import json
from core.broker.broker_manager import BrokerManager
from core.broker.message_buffer import MessageBuffer, ConnectionPool
import csv

class Main:
    def __init__(self) -> None:
        print('STARTING!!!')
        config = Config()
        self.second_process()
        ##############################
        # 1
        # multi_parser = MultiParser()
        # multi_parser.run_title_parser(['https://gizmodo.com/tech/artificial-intelligence',
        #                                'https://syncedreview.com/category/popular/'])
        # 2
        # multi_parser.run_article_parser('https://www.scientificamerican.com/article/stanford-ai-index-rapid-progress/')

    def readCSV(self) -> list[any]:
        objects = []
        encoding = 'utf-8'

        with open('output.csv', 'r', newline='', encoding=encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                objects.append(row)
        return objects

    def callback(self, ch, method, properties, body):
        print('RECIVED')
        
        msg = json.loads(body)

        if msg['type'] == 'titles':
            print('TITLES!!!')
            multi_parser = MultiParser()
            multi_parser.run_title_parser(resources=msg['resources'])
        elif msg['resources'] in ['all', 'Scientificamerican', 'MIT', 'Extremetech']:
            multi_parser = MultiParser()
            multi_parser.run(site=msg['resource'])
        else:
            multi_parser = MultiParser()
            multi_parser.run()

    def second_process(self) -> None:
        queue_name = 'apiparser'
        broker = BrokerManager(queue_name, 'broker')
        broker.set_callback(self.callback)

        print(' [*] Waiting for messages.')
        broker.channel.start_consuming()

        # buffer = MessageBuffer()
        # connection_pool = ConnectionPool(host="localhost", queue_name=queue_name, buffer=buffer)
        # consumer_thread = threading.Thread(target=connection_pool.consume, args=(consume_callback,))
        # consumer_thread.start()


if __name__ == "__main__":
    print("starting main...")
    Main()