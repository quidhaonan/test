# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GraduationprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    third_level_name=scrapy.Field()
    name=scrapy.Field()
    price=scrapy.Field()
    start_batching=scrapy.Field()
    update_time=scrapy.Field()
    ship_from_address=scrapy.Field()
    purchasing_heat=scrapy.Field()
    inquiry=scrapy.Field()
    traded=scrapy.Field()
    assess=scrapy.Field()
    desc=scrapy.Field()
    shop_url=scrapy.Field()
    pass
