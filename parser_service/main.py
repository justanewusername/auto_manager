from bestconfig import Config
from core.parsers import MultiParser
from scrapy import cmdline
import json
from core.broker.broker_manager import BrokerManager
import csv

class Main:
    def __init__(self) -> None:
        config = Config()
        # self.second_process()
        ##############################
        multi_parser = MultiParser()
        multi_parser.run_title_parser(['https://gizmodo.com/tech/artificial-intelligence',
                                       'https://syncedreview.com/category/popular/'])
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
        multi_parser = MultiParser()
        msg = json.loads(body)

        if msg['type'] == 'titles':
            multi_parser.run_title_parser(resources=msg['resources'])

        if msg['resource'] in ['all', 'Scientificamerican', 'MIT', 'Extremetech']:
            multi_parser.run(site=msg['resource'])
        else:
            multi_parser.run()

    def second_process(self) -> None:
        queue_name = 'apiparser'
        broker = BrokerManager(queue_name, 'broker')
        broker.set_callback(self.callback)

        print(' [*] Waiting for messages.')
        broker.channel.start_consuming()


if __name__ == "__main__":
    Main()