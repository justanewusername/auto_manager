from scrapy.crawler import CrawlerProcess
from bestconfig import Config
from core.parsers.article_parsers import *
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings

class MultiParser:
    def __init__(self):
        config = Config()
        self.crawler_process = CrawlerProcess({
            'USER_AGENT': config['USER_AGENT']
        })

        self.parsers = {
            'SCIENTIFICAMERICAN': ScientificamericanParser,
            'MIT': MITParser,
            'EXTREMETECH': ExtremetechParser,
            'VENTUREBEAT': VenturebeatParser,
            'GIZMODO': GizmodoParser,
            'SYNCED': ExtremetechParser,
        }
    
    def run(self, site='ALL', days : int = 14) -> None:
        if site.upper() == 'ALL':
            for parser in self.parsers:
                self.crawler_process.crawl(parser, days=days)
        else:
            self.crawler_process.crawl(self.parsers[site.upper()], days=days)
        self.crawler_process.start()

    def run_title_parser(self, resource: str) -> None:
        self.crawler_process.crawl(UniversalTitleParser,
                                   start_urls=[resource])
        self.crawler_process.start()

    def run_article_parser(self, resource: str) -> None:
        self.crawler_process.crawl(UniversalArticleParser,
                                   start_urls=[resource])
        self.crawler_process.start()