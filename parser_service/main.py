from bestconfig import Config
from core.parsers import MultiParser
from scrapy import cmdline
import json
from core.broker.broker_manager import BrokerManager
from core.broker.progress_notifier import send_progress
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
        print('user id: ', msg['user_id'])

        if msg['type'] == 'titles':
            print('TITLES!!!')
            multi_parser = MultiParser()
            multi_parser.run_title_parser(resources=msg['resources'], user_id=msg['user_id'])
        elif msg['type'] == 'articles':
            multi_parser = MultiParser()
            multi_parser.run_article_parser(msg['resources'], msg['user_id'])
        elif msg['resources'] in ['all', 'Scientificamerican', 'MIT', 'Extremetech']:
            multi_parser = MultiParser()
            multi_parser.run(site=msg['resource'])
        else:
            multi_parser = MultiParser()
            multi_parser.run()
        print("__________END__________")
        print("__________END__________")
        print("__________END__________")
        send_progress(msg['user_id'], 'done')
        

    def second_process(self) -> None:
        queue_name = 'apiparser'
        broker = BrokerManager(queue_name, 'broker')
        broker.set_callback(self.callback)

        print(' [*] Waiting for messages.')
        broker.channel.start_consuming()


if __name__ == "__main__":
    print("starting main...")
    Main()