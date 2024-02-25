import csv
from bestconfig import Config
from scrapy.exporters import CsvItemExporter
import mysql.connector
from core.database_manager import DatabaseManager
import json
from bs4 import BeautifulSoup
from core.broker.broker_manager import BrokerManager
import tiktoken


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

class BrokerPipeline:
    def process_item(self, item, spider):
        if 'content' in item:
            soup = BeautifulSoup(item['content'], 'html.parser')
            if soup.find(True):
                print("найден тэг")
                return ""
            queue_name = 'articles'
            broker = BrokerManager(queue_name, 'broker')
            msg = json.dumps({'content': item['content'], 'title': item['title'], 'url': item['url'], 'destination': 'posts'})
            broker.send_msg(msg)
            # broker.channel.basic_publish(exchange='', routing_key=queue_name, body=msg)
            # broker.connection.close()
            broker.close()
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

# сохранение в БД
class MySQLPipeline:
    def __init__(self, host, database, user, password):
        # настройки БД
        config = Config()
        
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        insert_query = "INSERT INTO articles (title, content) VALUES (%s, %s)"
        data = (item['title'], item['content'])
        cursor.execute(insert_query, data)
        self.conn.commit()
        cursor.close()
        return item