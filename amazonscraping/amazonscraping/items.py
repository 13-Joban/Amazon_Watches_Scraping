# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonscrapingItem(scrapy.Item):
    # define the fields for your item here like:
    product_rank = scrapy.Field(serializer=int)
    product_brand = scrapy.Field()
    product_description = scrapy.Field()
    product_case_diameter = scrapy.Field()
    product_band_color = scrapy.Field()
    product_band_material_type = scrapy.Field()
    product_watch_movement_type = scrapy.Field()
    product_warranty_type = scrapy.Field()
    product_case_thickness = scrapy.Field()
    product_item_weight = scrapy.Field()
    product_country_of_origin = scrapy.Field()
    product_price = scrapy.Field()
    product_url = scrapy.Field()
