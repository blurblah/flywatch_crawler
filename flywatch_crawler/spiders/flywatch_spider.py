import scrapy
import time
from flywatch_crawler.items import FlywatchCrawlerItem

class FlyWatchSpider(scrapy.Spider):
	BASE_URL = "http://flywatch.co.kr/board/"
	index = 0

	name = "flywatch"
	start_urls = [
		"http://flywatch.co.kr/board/board.html?code=flywatch_image1",
		"http://flywatch.co.kr/board/board.html?code=flywatch_image3",
		"http://flywatch.co.kr/board/board.html?code=flywatch_image4"
	]

	def parse(self, response):
		#//table[@class="bl_unit"]
		#/td[@class="bl_subject bl_list"]
		#/td[@class="bl_date bl_list"]
		itemList = list()
		for sel in response.xpath('//table[@class="bl_unit"]'):
			item = FlywatchCrawlerItem()
			url = sel.css("td.bl_subject a::attr('href')").extract()[0]
			item['url'] = self.BASE_URL + url
			item['createdAt'] = sel.css("td.bl_date span::text").extract()[0]
			yield scrapy.Request(item['url'], callback = self.parseDetails, meta = {'item': item})
			#time.sleep(2)
			#itemList.append(item)

		#for item in itemList:
		#	print "########", item['url']
		#	time.sleep(1)
		#	yield scrapy.Request(item['url'], callback = self.parseDetails, meta = {'item': item})

	def parseDetails(self, response):
		self.index += + 1
		# title : td id bv_subject text
		# createdAt : td id bv_writedate text
		# contents : div id bc_contentview text
		item = response.meta['item']
		item['title'] = "".join(response.css("td#bv_subject::text").extract()).lstrip().rstrip()
		content = "".join(response.css("div#bv_contentview::text").extract())
		item['content'] = content.lstrip().rstrip().replace('\r', '').replace('\n', '')

		print "####", self.index, "####"
		print "title:", item['title']
		print "url:", item['url']
		print "createdAt:", item['createdAt']
		print "content:", item['content']
		print "#######"

		yield item