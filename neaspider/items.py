# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProvincepageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
    Container for province page, this page display and store
    all link conducted to dam description page
    """
    Province = scrapy.Field()
    DamType = scrapy.Field()
    DamLink = scrapy.Field()

class DampageItem(scrapy.Item):
    """
    Container for dam description page, this page display the dam's photograph
    and its basic information
    """
    Province = scrapy.Field()
    DamName = scrapy.Field()
    DamType = scrapy.Field()
    DamDescription = scrapy.Field()
    DamLink = scrapy.Field()
