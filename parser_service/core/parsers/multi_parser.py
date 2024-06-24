from scrapy.crawler import CrawlerProcess
from bestconfig import Config
from core.parsers.article_parsers import *
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from multiprocessing import Process, Queue
from twisted.internet import reactor
import scrapy.crawler as crawler

class MultiParser:
    def __init__(self):
        self.config = Config()
        # self.crawler_process = CrawlerProcess({
        #     'USER_AGENT': self.config['USER_AGENT']
        # })

        self.parsers = {
            'SCIENTIFICAMERICAN': ScientificamericanParser,
            'MIT': MITParser,
            'EXTREMETECH': ExtremetechParser,
            'VENTUREBEAT': VenturebeatParser,
            'GIZMODO': GizmodoParser,
            'SYNCED': ExtremetechParser,
        }
    
    def run_spider(self, spider, days=None, user_id=None, start_urls=None):
        def f(q):
            try:
                runner = crawler.CrawlerRunner()
                deferred = runner.crawl(spider, days=days, user_id=user_id, start_urls=start_urls)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run()
                q.put(None)
            except Exception as e:
                q.put(e)

        q = Queue()
        p = Process(target=f, args=(q,))
        p.start()
        result = q.get()
        p.join()

        if result is not None:
            raise result
    

    def rerun_crawler(self):
        self.crawler_process = CrawlerProcess({
            'USER_AGENT': self.config['USER_AGENT']
        })

    def run(self, site='ALL', days : int = 14) -> None:
        if site.upper() == 'ALL':
            for parser in self.parsers.values():
                self.run_spider(spyder=parser, days=days)
        else:
            self.run_spider(spyder=self.parsers[site.upper()], days=days)


    def run_title_parser(self, resources: list[str], user_id: int) -> None:
        self.run_spider(spider=UniversalTitleParser, start_urls=resources, user_id=user_id)


    def run_article_parser(self, url: str, user_id: int) -> None:
        self.run_spider(spider=UniversalArticleParser, start_urls=[url], user_id=user_id)
        
