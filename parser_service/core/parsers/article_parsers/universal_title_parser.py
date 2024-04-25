from time import process_time_ns
import scrapy
from datetime import datetime
from dateutil import parser
from urllib.parse import urlparse

class UniversalTitleParser(scrapy.Spider):
    name = 'Universal title Parser'
    start_urls = ['https://gizmodo.com/tech/artificial-intelligence']
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         # 'core.parsers.article_parsers.pipelines.RequestSenderPipeline': 300,
    #     },
    # }

    def __init__(self, *args, **kwargs):
        print('00000000000')
        super(UniversalTitleParser, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', ['https://gizmodo.com/tech/artificial-intelligence'])
        self.days = kwargs.get('days', 14)
        self.category = kwargs.get('category', 'other')
        self.resource = kwargs.get('resource', 'other')

    
    def parse(self, response):
        print('woooooooooooooow')
        ARTICLE_TAG = 'article'
        days_difference = self.days

        articles = response.css(ARTICLE_TAG)
        print("ARTICLE COUNT:", len(articles))
        if len(articles) == 0:
            articles = response.css('li')
        
        right_title_pattern = self.find_right_title_pattern(article=articles[0])
        if right_title_pattern == '':
            yield ''

        for article in articles:
            right_title_pattern = self.find_right_title_pattern(article=article)
            title = article.css(right_title_pattern).extract()
            title = max(title, key=len)
            title = self.proccess_title(title)

            date_str = article.css('time ::attr(datetime)').get()
            if date_str is not None:
                print(date_str)
                date_object = parser.parse(date_str)
                today = datetime.now().date()
                
                if (today - date_object.date()).days > days_difference:
                    break
            
            url = self.find_right_url_pattern(article)

            url = self.process_url(url, response.url)
            
            print('77777777')
            yield {
                'title': title,
                'url': url,
                'category': self.category,
                'resource': self.resource,
                'last_update': datetime.today().strftime('%d.%m.%Y'),
            }


    def find_right_title_pattern(self, article):
        right_pattern = ''
        title_tags = ['h2', 'h3', 'h4']
        for title_tag in title_tags:
            if ''.join(article.css(title_tag + " ::text").extract()) is not None:
                if len(''.join(article.css(title_tag + " ::text").extract())) > 10:
                    right_pattern = title_tag + " ::text"
                    print(right_pattern)
                    break
        if right_pattern == '':
            if ''.join(article.css("a ::text").extract()) is not None:
                right_pattern = 'a ::text'
        return right_pattern


    def find_right_url_pattern(self, article):
        title_tags = ['h2', 'h3', 'h4']
        result = ''
        for title_tag in title_tags:
            print('111')
            if len(article.css(title_tag)) != 0:
                print('222')
                if len(article.css(title_tag + ' a')) != 0:
                    print('333')
                    result = article.css(title_tag + ' a').attrib['href']
                    break
                parent_element = article.xpath('.//' + title_tag + '/..')
                print('444')
                print(parent_element)
                if len(parent_element.css('a')) == 0:
                    print('555')
                    parent_element = article.xpath('.//' + title_tag + '/../..')
                    if len(parent_element.css('a')) == 0:
                        print('666')
                        result = article.css('a').attrib['href']
                        break
                    else:
                        print('777')
                        result = parent_element.css('a').attrib['href']
                        break
                else:
                    print('888')
                    print(parent_element.css('a').attrib['href'])
                    result = parent_element.css('a').attrib['href']
                    break
        if result == '':
            print('999')
            result = article.css('a').attrib['href']
        print('AAA ' + result)
        return result

    def find_right_article_pattern(self):
        pass


    def proccess_title(self, title: str):
        title = title.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
        title = title.strip()
        return title
    
    def process_url(self, url: str, response_url: str):
        parsed_url = urlparse(response_url)
        base_url = parsed_url.scheme + "://" + parsed_url.netloc
        if url[0] != 'h':
            if url[0] != '/':
                url = '/' + url
            url = base_url + url
        return url
