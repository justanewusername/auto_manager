from time import process_time_ns
import scrapy
from datetime import datetime
from dateutil import parser
from urllib.parse import urlparse
from core.broker.progress_notifier import send_progress

class UniversalTitleParser(scrapy.Spider):
    name = 'Universal title Parser'
    start_urls = ['https://gizmodo.com/tech/artificial-intelligence']
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.parsers.article_parsers.pipelines.TitlePostgresPipeline': 300,
        },
    }


    def __init__(self, *args, **kwargs):
        super(UniversalTitleParser, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', ['https://gizmodo.com/tech/artificial-intelligence'])
        self.days = kwargs.get('days', 14)
        self.category = kwargs.get('category', 'other')
        self.resource = kwargs.get('resource', 'other')
        self.user_id = kwargs.get('user_id', '1')

    
    def parse(self, response):
        ARTICLE_TAG = 'article'
        days_difference = self.days

        articles = response.css(ARTICLE_TAG)

        current_article_index = 1

        if len(articles) == 0:
            articles = response.css('li')
        
        right_title_pattern = self.find_right_title_pattern(article=articles[0])
        if right_title_pattern == '':
            yield ''

        for article in articles:
            
            send_progress(user_id=self.user_id, status='progress')

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

            current_article_index += 1
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
            if len(article.css(title_tag)) != 0:
                if len(article.css(title_tag + ' a')) != 0:
                    result = article.css(title_tag + ' a').attrib['href']
                    break
                parent_element = article.xpath('.//' + title_tag + '/..')
                if len(parent_element.css('a')) == 0:
                    parent_element = article.xpath('.//' + title_tag + '/../..')
                    if len(parent_element.css('a')) == 0:
                        result = article.css('a').attrib['href']
                        break
                    else:
                        result = parent_element.css('a').attrib['href']
                        break
                else:
                    result = parent_element.css('a').attrib['href']
                    break
        if result == '':
            result = article.css('a').attrib['href']
        return result


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
