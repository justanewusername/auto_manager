from bestconfig import Config
from core.parsers.article_parsers import ScientificamericanParser, MITParser
from scrapy.crawler import CrawlerProcess
from core.parsers import MultiParser
from core.schedule.schedule import Schedule
import csv

def readCSV():
    objects = []
    encoding = 'utf-8'

    with open('output.csv', 'r', newline='', encoding=encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            objects.append(row)
    return objects


def main():
    config = Config()
    print(config['version'])
    
    interval_days = 7
    
    # start schedule
    schedule = Schedule(run_parsers, interval_days)
    schedule.run()
    
    # articles = readCSV()
    
    # print(len(articles))
    # # print(articles[0]['title'])
    # # print(articles[0]['content'])
    

def run_parsers():
    multiParser = MultiParser()
    multiParser.run()

if __name__ == '__main__':
    main()
    
