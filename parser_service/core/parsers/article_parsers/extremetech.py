import scrapy
import pytz
from datetime import datetime, timezone

class ExtremetechParser(scrapy.Spider):
    name = 'scientificamerican-scryper'
    start_urls = ['https://www.extremetech.com/tag/artificial-intelligence/page/2']
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.parsers.article_parsers.pipelines.CleaningPipeline': 300,
            'core.parsers.article_parsers.pipelines.CsvExportPipeline': 400,
            'core.parsers.article_parsers.pipelines.PostgresPipeline': 450,
            'core.parsers.article_parsers.pipelines.BrokerPipeline': 500,
        },
    }
    
    def parse(self, response):
        articles = response.css('main section section')
        ARTICLE_TAG = '.item.flex.mt-4'
        days_difference = self.settings.get('days_difference', 15)
        for article in articles.css(ARTICLE_TAG):
            article_url = article.css('a').attrib['href']
            article_date = article.css('time ::attr(datetime)').get()
            print(article_date)
            print(article_date[:-6])
            article_date = article_date[:-6]
            date_format = '%a, %d %b %Y %H:%M:%S'
            article_date = datetime.strptime(article_date, date_format)

            now_date = datetime.now()
            # date checking
            if (now_date - article_date).days > days_difference:
                continue
            yield response.follow('https://www.extremetech.com/tag/artificial-intelligence' + article_url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        content = " ".join(response.css('main section .editor-content ::text').getall())

        yield {
            'title': title,
            'content': content,
            'url': response.request.url,
        }
