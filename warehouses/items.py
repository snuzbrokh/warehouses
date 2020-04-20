# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WarehousesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    status = scrapy.Field()
    price = scrapy.Field()
    propType = scrapy.Field()
    subType = scrapy.Field()
    spaces = scrapy.Field()
    spaceAvailable = scrapy.Field()
    buildingSize = scrapy.Field()


    extraInfo = scrapy.Field()

    listingDate = scrapy.Field()
    listingID = scrapy.Field()

    amenities = scrapy.Field()
    utilities = scrapy.Field()

    transport = scrapy.Field()

    #tax_dict = scrapy.Field()

