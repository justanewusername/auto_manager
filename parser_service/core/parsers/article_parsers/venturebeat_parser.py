import scrapy
from datetime import datetime

class VenturebeatParser(scrapy.Spider):
    name = 'Venturebeat Parser'
    start_urls = ['https://venturebeat.com/category/ai/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.parsers.article_parsers.pipelines.CleaningPipeline': 300,
            'core.parsers.article_parsers.pipelines.CsvExportPipeline': 400,
            # 'core.parsers.article_parsers.pipelines.PostgresPipeline': 450,
            'core.parsers.article_parsers.pipelines.BrokerPipeline': 500,
        },
    }
    
    def parse(self, response):
        articles = response.css('.MainBlock')
        ARTICLE_TAG = 'article'
        days_difference = self.settings.get('days_difference', 20)
        
        for article in articles.css(ARTICLE_TAG):
            article_url = article.css('h2 a').attrib['href']
            article_date = article.css('time ::text').get()
            article_date = datetime.strptime(article_date, "%B %d, %Y %I:%M %p")
            
            # date checking
            if (datetime.today() - article_date).days > days_difference:
                continue
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        content = " ".join(response.css('article ::text').getall())

        yield {
            'title': title,
            'content': content,
            'url': response.request.url,
            'category': 'AI',
            'resource': 'venturebeat'
        }