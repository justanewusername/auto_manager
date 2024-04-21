import scrapy
from datetime import datetime

class UniversalTitleParser(scrapy.Spider):
    name = 'Universal title Parser'
    start_urls = ['https://gizmodo.com/tech/artificial-intelligence']
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.parsers.article_parsers.pipelines.RequestSenderPipeline': 300,
        },
    }

    def __init__(self, *args, **kwargs):
        super(UniversalTitleParser, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', ['https://gizmodo.com/tech/artificial-intelligence'])
        self.days = kwargs.get('days', 14)
    
    def parse(self, response):
        ARTICLE_TAG = 'article'
        days_difference = self.days

        articles = []
        for article in response.css(ARTICLE_TAG):
            article_url = article.css('a').attrib['href'].get()
            article_title = article.css('a ::text').get()
            articles.append({'title': article_title, 'url': article_url})
        yield articles