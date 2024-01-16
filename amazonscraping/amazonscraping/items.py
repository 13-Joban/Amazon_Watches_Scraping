# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonscrapingItem(scrapy.Item):
    # define the fields for your item here like:
    product_brand = scrapy.Field()
    product_desc = scrapy.Field()
    product_price = scrapy.Field()
    product_url = scrapy.Field()
