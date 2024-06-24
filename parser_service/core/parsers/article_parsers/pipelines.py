import csv
from bestconfig import Config
from scrapy.exporters import CsvItemExporter
from core.database_manager import DatabaseManager
import json
from bs4 import BeautifulSoup
from core.broker.broker_manager import BrokerManager
import tiktoken
import requests


class CleaningPipeline:
    def process_item(self, item, spider):
        if 'content' in item:
            cleaned_content = item['content'].replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
            item['content'] = cleaned_content

            # checking token limit
            tokens_count = self.num_tokens_from_string(item['content'])

            max_length = 12000
            if tokens_count > 4000:
                item['content'] = item['content'][:max_length]
        return item

    def num_tokens_from_string(self, string: str) -> int:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        num_tokens = len(encoding.encode(string))
        return num_tokens

# class BrokerPipeline:
#     def process_item(self, item, spider):
#         if 'content' in item:
#             soup = BeautifulSoup(item['content'], 'html.parser')
#             if soup.find(True):
#                 return ""
#             queue_name = 'articles'
#             broker = BrokerManager(queue_name, 'broker')
#             msg = json.dumps({'content': item['content'], 
#                               'title': item['title'], 
#                               'url': item['url'], 
#                               'destination': 'posts',
#                               'category': item['category'],
#                               'resource': item['resource']})
#             broker.send_msg(msg)
#             broker.close()
#         return item

class BrokerPipeline:
    def process_item(self, item, spider):
        if 'content' in item:
            soup = BeautifulSoup(item['content'], 'html.parser')
            if soup.find(True):
                return ""
            queue_name = 'articles'
            broker = BrokerManager(queue_name, 'broker')
            msg = json.dumps({'content': item['content'],
                              'user_id': item['user_id'],
                              'destination': 'posts',
                              })
            broker.send_msg(msg)
            broker.close()
        return item

class RequestSenderPipeline:
    def process_item(self, item, spider):
        url = 'http://localhost:8811/posts/titles' # http://185.233.81.221:8811/posts/titles
        if 'title' in item:
            requests.post(url, json = item)
        return item


# сохранение в файл
class CsvExportPipeline:
    def __init__(self):
        self.file = open('output.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, include_headers_line=True)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class PostgresPipeline:
    def __init__(self):
        self.db_manager = DatabaseManager('postgresql://user:qwerty@db:5432/mydbname')

    def process_item(self, item, spider):
        self.db_manager.create_post(article=item['content'], title=item['title'], url=item['url'])
        return item
    

class TitlePostgresPipeline:
    def __init__(self):
        self.db_manager = DatabaseManager('postgresql://user:qwerty@db:5432/mydbname')

    def process_item(self, item, spider):
        print("i'm here!!!!")
        self.db_manager.create_post(title=item['title'], url=item['url'])
        print("Nice!")
        return item


# class TitlePostgresPipeline:
#     def __init__(self):
#         self.db_manager = DatabaseManager('postgresql://user:qwerty@db:5432/mydbname')

#     def process_item(self, item, spider):
#         self.db_manager.create_title(title=item['title'], url=item['url'],
#                                      category=item['category'], resource=item['resource'],
#                                      last_update=item['last_update'])
#         return item