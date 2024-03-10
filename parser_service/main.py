from bestconfig import Config
from core.parsers.article_parsers import ScientificamericanParser, MITParser
from scrapy.crawler import CrawlerProcess
from core.parsers import MultiParser
from core.schedule.schedule import Schedule
import multiprocessing
import threading
import time
from scrapy import cmdline
import json
from core.broker.broker_manager import BrokerManager
import csv

def readCSV():
    objects = []
    encoding = 'utf-8'

    with open('output.csv', 'r', newline='', encoding=encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            objects.append(row)
    return objects


def run_scrapy():
    # cmdline.execute("scrapy runspider ./core/parsers/article_parsers/MIT_parser.py".split())
    cmdline.execute("scrapy runspider ./core/parsers/article_parsers/venturebeat_parser.py".split())

def run_parsers(site='all'):
    multiParser = MultiParser()
    multiParser.run(site=site)

def callback(ch, method, properties, body):
    print("recived")
    print(body)
    
    msg = json.loads(body)
    if msg['resource'] in ['all', 'Scientificamerican', 'MIT', 'Extremetech']:
        run_scrapy()
    else:
        run_scrapy()

def second_process():
    queue_name = 'apiparser'
    broker = BrokerManager(queue_name, 'broker')
    broker.set_callback(callback)

    print(' [*] Waiting for messages.')
    broker.channel.start_consuming()

def main():
    config = Config()
    print(config['version'])
    
    interval_days = 14

    # s_process = multiprocessing.Process(target=second_process)
    # s_process.start()

    # run_parsers()
    second_process()

    # start schedule
    # schedule = Schedule(run_parsers, interval_days)
    # schedule.run()
    
    # articles = readCSV()
    
    # print(len(articles))
    # print(articles[0]['title'])
    # # print(articles[0]['content'])


###########################################
###########################################
###########################################

if __name__ == "__main__":
    main()