# -*- coding: utf-8 -*-
from uav.spiders.uavSpider import uavSpider
from scrapy.utils.project import get_project_settings  
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

settings = get_project_settings()  
process = CrawlerProcess(settings)
process.crawl(uavSpider)
process.start()