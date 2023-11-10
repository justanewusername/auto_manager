BOT_NAME = 'my_scraper'
ITEM_PIPELINES = {
    'core.parsers.article_parsers.CleaningPipeline': 300,
}