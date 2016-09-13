# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.http import FormRequest
from uav.items import *
from scrapy.utils.url import urljoin_rfc,re


class uavSpider(CrawlSpider):
    name = 'uavSpider'
    allowed_domains = ['wrjzj.com',]
    start_urls = [r'http://www.wrjzj.com']

    rules = (
        # 同意进的页面
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #Rule(LinkExtractor(allow=('\d+\.html',),deny=('wrjgs/*','wrjdq/*','wrjtp/*','club/*','forum','wrjsp',)), callback='parse_item'),
        Rule(LinkExtractor(allow=('/\d+\.html',),deny=('wrjgs/*','wrjdq/*','wrjtp/*','club/*','forum','wrjsp',)), callback='parse_item'),
        Rule(LinkExtractor(allow=('wrjxw/','wrjyy/','wrjzc/','wrjjs/*')),),
    )
  
    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        item = UavArticle()
        item['title'] = response.xpath('//*[@id="xw_title"]/h1/a/text()').extract()[0]
        item['originUrl']   = response.url
        item["author"]      = response.xpath('//*[@id="xw_xinxi"]/span[2]/text()').re(u"编辑：(.+)")[0]
        item["content"]     = response.xpath('//*[@id="xw_content"]').extract()[0]
        item["images"]      = response.xpath('//*[@id="MyContent"]/p/img/@src').extract()
        item["Column"]      = response.xpath('//*[@id="xw_xinxi"]/span[4]/a/text()').extract()[0]
        item["types"]       = response.xpath('//*[@id="content"]/div[1]/a[2]/text()').extract()[0]
        

        #若有图片，判断是否需要对图片补充domain
        if 'images' in item:
            newimglist = []
            for img in item['images']:
                newimg={"path":img}
                if not re.search('http://', img):
                    newimg["url"] = urljoin_rfc(response.url, img)
                else:
                    newimg["url"] = img
                newimglist.append(newimg)
            item['images'] = newimglist

        return item
