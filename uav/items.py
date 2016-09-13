# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class UavItem(Item):
    # define the fields for your item here like:
    title = Field()
    link  = Field()



    
class UavArticle(Item):
    '''
    长文本，如游记 攻略
    ''' 
    Column=Field()      #栏目
    title = Field()     #标题
    author = Field()    #作者
    tags = Field()          #标签
    types = Field()         #类型
    content = Field()       #文章内容
    publishDate = Field()   #发表日期
    originUrl = Field()     #文章原始链接 用于搜索引擎爬虫的快照爬取
    abstract = Field()      #文章摘要
    pvNum = Field()          #浏览量
    keyWords = Field()       #关键字  

    
    images = Field()        #图片原始链接列表

    md5=Field()             #MD5值
    isDup=Field()           #标识是否重复    
    densDic = Field()       #密度字典（xpath，文本密度，文本长度，标签密度，标签个数）
 


