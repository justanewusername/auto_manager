import csv
from bestconfig import Config
from scrapy.exporters import CsvItemExporter
import mysql.connector


class CleaningPipeline:
    def process_item(self, item, spider):
        if 'content' in item:
            cleaned_content = item['content'].replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
            item['content'] = cleaned_content
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