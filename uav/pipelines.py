# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem ,CloseSpider
from scrapy.http.request import Request
from twisted.enterprise import adbapi             #导入twisted的包
import MySQLdb
import MySQLdb.cursors
#import redis

class UavPipeline(object):
    def process_item(self, item, spider):
        if 'content' in item:
            return item
        else:
            raise DropItem("Missing link in %s" % item)

    def open_spider(self, spider):
        print("---------open_spider---------")



class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        self.cur.execute("select count(*) from wrjzj where originurl='%s'" % (item['originUrl']) )
        
        if self.cur.fetchone()[0] > 0:
            raise DropItem("Duplicate item found: %s" % item["originUrl"])
        else:
            return item

        #if self.Redis.exists('%s' % item['originUrl']):
        #    raise DropItem("Duplicate item found: %s" % item["originUrl"])
        #else:
        #    self.Redis.set('%s' % item['originUrl'],1)
        #    return item

    def __init__(self):
        try:
            #self.Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
            self.conn= MySQLdb.connect(
                    host='localhost',
                    port = 3306,
                    user='xing',
                    passwd='huhuhu',
                    db ='uavspiders',
                    )
            self.cur = self.conn.cursor()

        except Exception as e:
            print(e)
            raise CloseSpider("StrictRedis faild");
        

class mySQLPipeline(object):
    def __init__(self):                           #初始化连接mysql的数据库相关信息
        self.dbpool = adbapi.ConnectionPool(
            dbapiName='MySQLdb',
            host='localhost',
            db = 'uavspiders',
            user = 'xing',
            passwd = 'huhuhu',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
        )

    # pipeline dafault function                   #这个函数是pipeline默认调用的函数
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    # insert the data to databases                 #把数据插入到数据库中
    def _conditional_insert(self, tx, item):
        #sql = "insert into book values (%s, %s)"
        #tx.execute(sql,(item["title"], item["originUrl"][0:]))
        sql = "insert IGNORE into wrjzj (title,author,md5,types,originurl,content) values (%s,%s,%s,%s,%s,%s)"
        tx.execute(sql,(item["title"], 
                        item["author"],
                        "",
                        item["types"],
                        item["originUrl"],
                        item["content"])
        )



class UavImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['images']:
            print("----------download-------------")
            print(image_url)
            #因为在下面的file_path方法中获得不到mm的姓名，所以在这里把mm的姓名作为meta传过去
            yield Request(image_url["url"], meta={'path': image_url["path"]})

    def item_completed(self, results, item, info):
        return super(UavImagesPipeline, self).item_completed(results, item, info)

    def file_path(self, request, response=None, info=None):
        return request.meta['path']
        #f_path = super(UavImagesPipeline, self).file_path(request, response, info)
        #print("-----------------f_path---------------")
        #print(f_path)
        #f_path = f_path.replace('full', request.meta['path'], 1)#从meta取出mm的姓名作为文件夹名称
        #return f_path
        #pass