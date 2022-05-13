# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SecondProjectItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    document_id = scrapy.Field()
    author = scrapy.Field()
    authors = scrapy.Field()
    tags = scrapy.Field()
    abstract = scrapy.Field()
    publication_date = scrapy.Field()
    fulltext = scrapy.Field()
    fulltext_content_type = scrapy.Field()
    raw_content = scrapy.Field()
    raw_content_type = scrapy.Field()
    topic_id = scrapy.Field()
    product_category_id = scrapy.Field()
    type_id = scrapy.Field()
    seed_url = scrapy.Field()
    references = scrapy.Field()
    application_date = scrapy.Field()
    labels = scrapy.Field()
