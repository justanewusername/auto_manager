from scrapy.crawler import CrawlerProcess
from bestconfig import Config
from core.parsers.article_parsers import ScientificamericanParser, MITParser, ExtremetechParser
from scrapy.utils.project import get_project_settings

class MultiParser:
    def __init__(self):
        config = Config()
        self.crawler_process = CrawlerProcess({
            'USER_AGENT': config['USER_AGENT']
        })
    
    def run(self):
        self.crawler_process.crawl(ScientificamericanParser)
        self.crawler_process.crawl(MITParser)
        self.crawler_process.crawl(ExtremetechParser)
        self.crawler_process.start()