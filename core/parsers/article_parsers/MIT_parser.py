import scrapy
from datetime import datetime

class MITParser(scrapy.Spider):
    name = 'scientificamerican-scryper'
    start_urls = ['https://news.mit.edu/topic/artificial-intelligence2/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.parsers.article_parsers.pipelines.CleaningPipeline': 300,
            'core.parsers.article_parsers.pipelines.CsvExportPipeline': 400,
        },
    }
    
    def parse(self, response):
        articles = response.css('.page-term--views--list')
        ARTICLE_TAG = 'article'
        days_difference = 7
        
        for article in articles.css(ARTICLE_TAG):
            article_url = article.css('h3 a').attrib['href']
            article_date = article.css('time ::text').get()
            article_date = datetime.strptime(article_date, "%B %d, %Y")
            
            # date checking
            if (datetime.today() - article_date).days > days_difference:
                continue
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1 span::text').get()
        content = " ".join(response.css('.news-article--content .news-article--content--body ::text').getall())

        yield {
            'title': title,
            'content': content,
        }