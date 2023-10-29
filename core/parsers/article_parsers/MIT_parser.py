import scrapy

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
        print('starting')
        
        for article in articles.css(ARTICLE_TAG):
            article_url = article.css('h3 a').attrib['href']
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1 span::text').get()
        content = " ".join(response.css('.news-article--content .news-article--content--body ::text').getall())

        yield {
            'title': title,
            'content': content,
        }