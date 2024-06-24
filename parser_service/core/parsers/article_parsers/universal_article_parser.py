import scrapy

class UniversalArticleParser(scrapy.Spider):
    name = 'UniversalArticleParser-scryper'
    start_urls = ['https://www.scientificamerican.com/artificial-intelligence/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.parsers.article_parsers.pipelines.CleaningPipeline': 300,
            # 'core.parsers.article_parsers.pipelines.CsvExportPipeline': 400,
            # 'core.parsers.article_parsers.pipelines.PostgresPipeline': 450,
            'core.parsers.article_parsers.pipelines.BrokerPipeline': 500,
        },
    }

    def __init__(self, *args, **kwargs):
        super(UniversalArticleParser, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', ['https://www.scientificamerican.com/artificial-intelligence/'])
        self.days = kwargs.get('days', 20)
        self.user_id = kwargs.get('user_id', None)
        print('11111111111111111111111111111111111111111111111111')
    
    def parse(self, response):
            article_text = self.get_article_text(response)
            print('22222222222222222222222222222222222222222222222222222222222')
            yield {
                'content': article_text,
                'user_id': self.user_id,
            }


    def get_article_text(self, response):
        article_tag = 'article'
        if len(response.css(article_tag)) != 0:
            article_node = response.css(article_tag)
            if len(" ".join(article_node.xpath('.//p//text()').getall())) > 500:
                return " ".join(article_node.xpath('.//p//text()').getall())
        return " ".join(response.xpath('.//p//text()').getall())