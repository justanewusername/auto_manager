import scrapy
from datetime import datetime

class GizmodoParser(scrapy.Spider):
    name = 'Gizmodo_Parser'
    start_urls = ['https://gizmodo.com/tech/artificial-intelligence']
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.parsers.article_parsers.pipelines.CleaningPipeline': 300,
            'core.parsers.article_parsers.pipelines.CsvExportPipeline': 400,
            # 'core.parsers.article_parsers.pipelines.PostgresPipeline': 450,
            'core.parsers.article_parsers.pipelines.BrokerPipeline': 500,
        },
    }

    def __init__(self, *args, **kwargs):
        super(GizmodoParser, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', ['https://gizmodo.com/tech/artificial-intelligence'])
        self.days = kwargs.get('days', 14)
    
    def parse(self, response):
        articles = response.css('.jvChWP')
        articles = articles.css('main')
        ARTICLE_TAG = 'article'
        days_difference = self.days

        for article in articles.css(ARTICLE_TAG):
            article_url = article.css('.dYIPCV')
            article_url = article_url.css('a').attrib['href']
            article_date = article.css('time').attrib['datetime']
            article_date = datetime.strptime(article_date, "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None) 
            
            
            # date checking
            if (datetime.today() - article_date).days > days_difference:
                continue
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        content = response.css('.js_post-content')
        content = " ".join(content.css('p ::text').getall())

        yield {
            'title': title,
            'content': content,
            'url': response.request.url,
            'category': 'AI',
            'resource': 'gizmodo'
        }