from scrapy import Spider
from scrapy.http import Request
from warehouses.items import WarehousesItem
import xml.etree.ElementTree as ET 
import pandas as pd

def remove_tags(text): return ''.join(ET.fromstring(text).itertext())

class WarehousesSpider(Spider):
	name = 'warehouses_spider'
	start_urls = ['https://www.loopnet.com/warehouses-for-lease/']



	def parse(self, response):
		# Inital scrape looked at warehouses in every state
		states = ['alabama', 'arizona','alaska', 'arkansas', 'california', 'colorado', 'connecticut', \
		'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', \
		'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', \
		'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new-hampshire', 'new-jersey', \
		'new-mexico', 'new-york', 'north-carolina', 'north-dakota', 'ohio', 'oklahoma', 'oregon', \
		'pennsylvania', 'rhode-island', 'south-carolina', 'south-dakota', 'tennessee', 'vermont','wyoming',\
		'wisconsin','west virginia','washington','virginina','utah','texas']
		n = 0
		for state in ['new-mexico','']:

			result_urls = ['https://www.loopnet.com/{}_warehouses-for-lease/{}/'.format(state,i) for i in range(1,21)]
			for url in result_urls:
				try:
					yield Request(url = url, callback = self.parse_result_page)
				except:
					continue
		
	def parse_result_page(self, response):


		links = response.xpath('//div[@class="listingDescription"]/a/@href').extract()
		addresses = response.xpath('//div[@class="listingDescription"]/a/@title').extract()
		attributes = response.xpath('//table[@class="listingAttributes"]//tr/td[2]/text()').extract()
		names = ['address','status','price','propType','subType','spaces','spaceAvailable','buildingSize']

		attrs = [[addr]+attributes[i*7:7*(i+1)] for i,addr in enumerate(addresses)]
		meta = {link:attr for link,attr in zip(links,attrs)}

		for lnk, attr in meta.items():
			url = 'http://www.loopnet.com{}'.format(lnk)
			meta_dict = dict(zip(names,attr))

			try:
				yield Request(url = url, callback = self.parse_listing_page, meta = meta_dict)
			except:
				continue
		# for url in ['https://www.loopnet.com/{}'.format(link) for link in links][:2]:
		# 	yield Request(url = url, callback = self.parse_listing_page)
			
	def parse_listing_page(self, response):

		address, city, state = response.meta['address'].split(', ')

		temp = response.xpath('//section[@class="listing-features"]/table//tr//td//text()').extract()
		temp = [row.replace('\n','').strip() for row in temp]
		extraInfo = [a for a in temp if a != '']


		# offering_table = response.xpath('//section[@class="listing-features"]/table//tr').extract()
		# temp = [remove_tags(row).replace('\n','').strip() for row in offering_table]
		# offering_dict = dict([(temp[i],temp[i+1]) for i in range(0, len(temp)-1, 2)])

		timestamp = response.xpath('//ul[@class="property-timestamp"]//li/text()').extract()

		temp = response.xpath('//section[@class = "highlights include-in-page public-transportation-wrapper"]//section/table/tbody//tr//td//text()').extract()
		temp = [a.replace('\n','').strip() for a in temp]
		temp = [a for a in temp if a != '']
		transport = [tuple(temp[i:i+3]) for i in range(0,len(temp),3)]

		# temp = response.xpath('//section[@id="taxes"]//tr//td/text()').extract()
		# taxes = [remove_tags(a).replace('\n','').strip() for a in temp]
		# tax_dict = dict([(taxes[i], taxes[i+1]) for i in range(0,len(taxes)-1,2)])


		item = WarehousesItem()
		# Info pulled in from the results page
		item['address'] = address
		item['city'] = city
		item['state'] = state
		item['status'] = response.meta['status']
		item['price'] = response.meta['price']
		item['propType'] = response.meta['propType']
		item['subType'] = response.meta['subType']
		item['spaces'] = response.meta['spaces']
		item['spaceAvailable'] = response.meta['spaceAvailable']
		item['buildingSize'] = response.meta['buildingSize']

		## Info pulled in from the listing page
		item['highlights'] = response.xpath('//section[@class="highlights highlights--top include-in-page"]/div/ul//li/text()').extract()
		item['spaceSummary'] = response.xpath('//div[@id="available-spaces"]/div[2]/div/div[2]//p/text()').extract()
		item['spaceBullets'] = response.xpath('//div[@id="available-spaces"]/div[2]/div/div[2]//ul/li/text()').extract()
		item['extraInfo'] = extraInfo
		item['hoodMarket'] = response.xpath('//section[@class="neighborhood-market"]/div/div/div//p/text()').extract()
		item['propOverview'] = response.xpath('//section[@class="description about-address"]/div[2]/div/p/text()').extract()

		item['listingID'] = timestamp[0].strip()
		item['listingDate'] = timestamp[1].strip()
		item['amenities'] = response.xpath('//section[@class="highlights include-in-page features-and-amenities"]/div//ul/li/span/text()').extract()
		item['utilities'] = response.xpath('//section[@class="highlights include-in-page utilities"]//div/ul//li/text()').extract()
		item['transport'] = transport


		yield item 




