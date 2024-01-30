from bestconfig import Config
from core.parsers.article_parsers import ScientificamericanParser, MITParser
from scrapy.crawler import CrawlerProcess
from core.parsers import MultiParser
from core.schedule.schedule import Schedule
import multiprocessing
import time
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

def run_parsers():
    multiParser = MultiParser()
    multiParser.run()

def callback(ch, method, properties, body):
    print("recived")
    run_parsers()

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

    s_process = multiprocessing.Process(target=second_process)
    s_process.start()
    
    # start schedule
    schedule = Schedule(run_parsers, interval_days)
    schedule.run()
    
    # articles = readCSV()
    
    # print(len(articles))
    # print(articles[0]['title'])
    # # print(articles[0]['content'])


###########################################
###########################################
###########################################

if __name__ == "__main__":

    eternal_process = multiprocessing.Process(target=main)
    eternal_process.start()

    eternal_process.join()  # Ждем, пока вечный процесс не завершится
    print("all ended")