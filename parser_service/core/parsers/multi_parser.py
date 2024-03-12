from scrapy.crawler import CrawlerProcess
from bestconfig import Config
from core.parsers.article_parsers import ScientificamericanParser, MITParser, ExtremetechParser, SyncedParser, GizmodoParser, VenturebeatParser
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings

class MultiParser:
    def __init__(self):
        config = Config()
        self.crawler_process = CrawlerProcess({
            'USER_AGENT': config['USER_AGENT']
        })
    
    def run(self, site='all'):
        if site == 'all':
            self.crawler_process.crawl(ScientificamericanParser)
            self.crawler_process.crawl(MITParser)
            self.crawler_process.crawl(ExtremetechParser)
            self.crawler_process.crawl(VenturebeatParser)
            self.crawler_process.crawl(GizmodoParser, 
                                       start_urls=['https://gizmodo.com/tech/artificial-intelligence'], 
                                       days=14)
            self.crawler_process.start()
        elif site == 'Scientificamerican':
            self.crawler_process.crawl(ScientificamericanParser)
        elif site == 'MIT':
            self.crawler_process.crawl(MITParser)
        elif site == 'Extremetech':
            self.crawler_process.crawl(ExtremetechParser)
        elif site == 'Synced':
            self.crawler_process.crawl(ExtremetechParser)
