# -*- coding: utf-8 -*-

import redis
import time, MySQLdb      



conn=MySQLdb.connect(host="localhost",user="root",passwd="huhuhu",db="uavspiders",charset="utf8")    
cursor = conn.cursor()      


conn= MySQLdb.connect(
                    host='localhost',
                    port = 3306,
                    user='xing',
                    passwd='huhuhu',
                    db ='uavspiders',
                    )
cur = conn.cursor()


'''


# 初始化redis数据库连接
Redis = redis.StrictRedis(host='localhost',port=6379,db=0)

#查询      
n = cursor.execute("select title,originurl from wrjzj")      
for row in cursor.fetchall():      
    print row[0].encode("utf-8")
    print row[1].encode("utf-8")
    if Redis.exists(row[1]):
        print("已经存在")
    else:
        print(Redis.set(row[1],1))


'''