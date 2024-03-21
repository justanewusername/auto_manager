from bestconfig import Config
from core.parsers import MultiParser
from scrapy import cmdline
import json
from core.broker.broker_manager import BrokerManager
import csv

def readCSV() -> list[any]:
    objects = []
    encoding = 'utf-8'

    with open('output.csv', 'r', newline='', encoding=encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            objects.append(row)
    return objects


def run_scrapy() -> None:
    cmdline.execute("scrapy runspider ./core/parsers/article_parsers/venturebeat_parser.py".split())

def run_parsers(site : str ='all') -> None:
    multiParser = MultiParser()
    multiParser.run(site=site)

def run_title_parser(resource: str) -> None:
    multi_parser = MultiParser()
    multi_parser.run_title_parser(resource=resource)

def callback(ch, method, properties, body):
    msg = json.loads(body)

    if msg['type'] == 'titles':
        run_title_parser(msg['resource'])

    if msg['resource'] in ['all', 'Scientificamerican', 'MIT', 'Extremetech']:
        run_parsers(msg['resource'])
    else:
        run_parsers()

def second_process() -> None:
    queue_name = 'apiparser'
    broker = BrokerManager(queue_name, 'broker')
    broker.set_callback(callback)

    print(' [*] Waiting for messages.')
    broker.channel.start_consuming()

def main() -> None:
    config = Config()
    print(config['version'])
    
    second_process()


if __name__ == "__main__":
    main()