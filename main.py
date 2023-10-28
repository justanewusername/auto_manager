from bestconfig import Config
from core.parsers.article_parsers import ScientificamericanParser
from scrapy.crawler import CrawlerProcess
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
    
    
    # start scraper
    process = CrawlerProcess({
        'USER_AGENT': config['USER_AGENT']
    })

    # result = process.crawl(ScientificamericanParser)
    # process.start()
    
    articles = readCSV()
    
    print(len(articles))
    print(articles[0]['title'])
    print(articles[0]['content'])

if __name__ == '__main__':
    main()
    
