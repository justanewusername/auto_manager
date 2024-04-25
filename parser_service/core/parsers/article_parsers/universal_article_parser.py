import scrapy

class UniversalArticleParser(scrapy.Spider):
    name = 'UniversalArticleParser-scryper'
    start_urls = ['https://www.scientificamerican.com/artificial-intelligence/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.parsers.article_parsers.pipelines.CleaningPipeline': 300,
            'core.parsers.article_parsers.pipelines.CsvExportPipeline': 400,
            # 'core.parsers.article_parsers.pipelines.PostgresPipeline': 450,
            'core.parsers.article_parsers.pipelines.BrokerPipeline': 500,
        },
    }

    def __init__(self, *args, **kwargs):
        super(UniversalArticleParser, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', ['https://www.scientificamerican.com/artificial-intelligence/'])
        self.days = kwargs.get('days', 20)
    
    def parse(self, response):
            yield ''