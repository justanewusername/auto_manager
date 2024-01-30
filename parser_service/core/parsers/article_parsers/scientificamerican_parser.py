import scrapy

class ScientificamericanParser(scrapy.Spider):
    name = 'scientificamerican-scryper'
    start_urls = ['https://syncedreview.com/category/popular/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.parsers.article_parsers.pipelines.CleaningPipeline': 300,
            'core.parsers.article_parsers.pipelines.CsvExportPipeline': 400,
            'core.parsers.article_parsers.pipelines.BrokerPipeline': 500,
        },
    }
    
    def parse(self, response):
        ARTICLE_TAG = 'article'
        
        for article in response.css(ARTICLE_TAG):
            article_url = article.css('header h2 a').attrib['href']
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        content = " ".join(response.css('article ::text').getall())

        yield {
            'title': title,
            'content': content,
            'url': response.request.url,
        }