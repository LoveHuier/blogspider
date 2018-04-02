# -*- coding: utf-8 -*-
import pymysql
import codecs
import json


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BlogspiderPipeline(object):
    def __init__(self):
        """
        刚开始时，连接blog_spider数据库
        """
        self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="ts123456", db="blog_spider", port=3306)
        # self.file = codecs.open("/home/mata/dataex/blog_data.json", "wb", encoding='utf-8')

    def process_item(self, item, spider):
        """
        文章列表中，遍历每篇文章并进行处理。
        :param item:
        :param spider:
        :return:
        """
        for j in range(0, len(item['name'])):
            name = item['name'][j]
            url = item['url'][j]
            hits = item['hits'][j]
            comment = item['comment'][j]
            # body = {'name': name, 'url': url, 'hits': hits, 'comment': comment}
            # i = json.dumps(dict(body), ensure_ascii=False)
            # line = i + '\n'
            # self.file.write(line)

            # 通过query实现执行对应的sql语句
            # sql = 'insert into blogdata(name,url,hits,comment) values("songxh","111","222","333");'
            sql = "insert into blogdata(name,url,hits,comment) values('" + name + "','" + url + "','" + hits + "','" + comment + "');"
            cs = self.conn.cursor()
            cs.execute(sql)
            self.conn.commit()

        return item

    def close_spider(self, spider):
        """
        关闭数据库连接
        :param spider:
        :return:
        """
        self.conn.close()
        # self.file.close()
        print("DONE")
