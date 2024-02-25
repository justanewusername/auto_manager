import scrapy

class ScientificamericanParser(scrapy.Spider):
    name = 'scientificamerican-scryper'
    start_urls = ['https://www.scientificamerican.com/artificial-intelligence/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.parsers.article_parsers.pipelines.CleaningPipeline': 300,
            'core.parsers.article_parsers.pipelines.CsvExportPipeline': 400,
            # 'core.parsers.article_parsers.pipelines.PostgresPipeline': 450,
            'core.parsers.article_parsers.pipelines.BrokerPipeline': 500,
        },
    }
    
    def parse(self, response):
        ARTICLE_TAG = 'article'
        days_difference = self.settings.get('days_difference', 20)
        
        max_articles_count = 5

        current_article_index = 0
        for article in response.css(ARTICLE_TAG):
            article_url = article.css('a').attrib['href']

            current_article_index += 1
            if current_article_index > max_articles_count:
                break
            
            yield response.follow(article_url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        content = " ".join(response.css('article ::text').getall())

        yield {
            'title': title,
            'content': content,
            'url': response.request.url,
        }