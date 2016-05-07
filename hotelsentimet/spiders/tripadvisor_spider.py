
import scrapy
from hotelsentimet.items import HotelsentimetItem
from urlparse import urljoin

class TripadvisorSpider(scrapy.Spider):
  name = "tripadvisor"
  start_urls = [
      "https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html"
  ]
  def parse_review(self, response):
    item = HotelsentimetItem()
    item['title'] = response.xpath('//div[@class="quote"]/text()').extract()[0][1:-1] #strip the quotes (first and last char)
    item['content'] = response.xpath('//div[@class="entry"]/p/text()').extract()[0]
    item['stars'] = response.xpath('//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()[0]
    return item 

  def parse_hotel(self, response):
    for href in response.xpath('//div[@class="quote"]/a/@href'):
      url = urljoin(response.url, href.extract())
      #url = response.urljoin(href.extract())
      yield scrapy.Request(url, callback=self.parse_review)

    next_page = response.xpath('//div[@class="unified pagination "]/child::*[2][self::a]/@href')
    if next_page:
      url = urljoin(response.url, next_page[0].extract())
      #url = response.urljoin(next_page[0].extract())
      yield scrapy.Request(url, self.parse_hotel)

  def parse(self, response):
    for href in response.xpath('//div[@class="listing_title"]/a/@href'):
      url = urljoin(response.url, href.extract())
      #url = response.urljoin(href.extract())
      yield scrapy.Request(url, callback=self.parse_hotel)

    next_page = response.xpath('//div[@class="unified pagination standard_pagination"]/child::*[2][self::a]/@href')
    if next_page:
      url = urljoin(response.url, next_page[0].extract())
      #url = response.urljoin(next_page[0].extract())
      yield scrapy.Request(url, self.parse)
