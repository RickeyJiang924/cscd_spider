# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import pymysql
from scrapy.exceptions import DropItem
from cscd_spider import db_connection_pool as pool


class CscdSpiderPipeline(object):
    def process_item(self, item, spider):
        title = item.get("title")
        author = item.get("author")
        citation = item.get("citation")
        abstract = item.get("abstract")
        keywords = item.get("keywords")
        if title is None:
            raise DropItem("invalid item")
        self.insert(title, author, abstract, keywords, citation)
        return item

    def insert(self, title, author, abstract, keywords, citation):
        insert_sql = "insert into paper(title,author,abstract,keywords,citation) values (%s,%s,%s,%s,%s)" % (title, author, abstract, keywords, citation)
        with pool.get_db_connect() as db:
            db.cursor.execute(insert_sql)
            db.conn.commit()

