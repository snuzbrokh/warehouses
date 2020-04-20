from scrapy import Spider
from scrapy.http import Request
from warehouses.items import WarehousesItem
import xml.etree.ElementTree as ET 

def remove_tags(text): return ''.join(ET.fromstring(text).itertext())

class WarehousesSpider(Spider):
	name = 'myspider'
	#allowed_domains = ['loopnet.com/']
	start_urls = ('https://www.loopnet.com/new-york_warehouses-for-lease/1',
				  'https://www.loopnet.com/new-york_warehouses-for-lease/2')

def parse(self, response):
    # <processing code not shown>
    # collect `item_urls`
    for item_url in item_urls:
        yield scrapy.Request(item_url, self.parse_item)

def parse_item(self, response):
    # <processing code not shown>
    item = MyItem()
    # populate `item` fields
    # and extract item_details_url
    yield scrapy.Request(item_details_url, self.parse_details, cb_kwargs={'item': item})

def parse_details(self, response, item):
    # populate more `item` fields
    return item
	



    # landAssessment = scrapy.Field()
    # improveAssessment = scrapy.Field()
    # zoningCode = scrapy.Field()




