import pytz
from datetime import datetime, timezone


article_date = "Wed, 01 Nov 2023 21:22:52 +0000"
print(article_date)
print(article_date[:-6])
article_date = article_date[:-6]
date_format = '%a, %d %b %Y %H:%M:%S'
article_date = datetime.strptime(article_date, date_format)

print('11111111111111111111111111')
print(type(article_date))
now_date = datetime.now()
print(type(now_date))
print(now_date - article_date)
print((now_date - article_date).days)
print('***********************')