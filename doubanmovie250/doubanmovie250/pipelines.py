# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from doubanmovie250.items import Doubanmovie250Item
from twisted.enterprise import adbapi
import logging


class Doubanmovie250Pipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host = '127.0.0.1',
                                            db = 'movie250',
                                            user = 'root',
                                            passwd = '',
                                            cursorclass = MySQLdb.cursors.DictCursor,
                                            charset = 'utf8',
                                            use_unicode = True
                                            )

    def process_item(self, item, spider):
        querly = self.dbpool.runInteraction(self._conditional_insert,item)
        querly.addErrback(self.handle_error)
        return item

    def _conditional_insert(self,tx,item):
        if item.get('title'):
            # tx.execute("truncate table movie_info")
            rank = item["rank"][0]
            title = item["title"][0]
            link = item["link"][0]
            star = item["star"][0]
            rate = item["rate"][0]
            if item["quote"]:
                quote = item["quote"][0]
            else:
                quote = "暂无".decode("utf-8")
            type = item["type"][1].strip()

            tx.execute(\
                "insert into movie_info (movie_rank,movie_title,movie_link,movie_star,movie_rate,movie_quote,movie_type)\
                value (%s,%s,%s,%s,%s,%s,%s)",
                (
                    rank,
                    title,
                    link,
                    star,
                    rate,
                    quote,
                    type

                )
                )
    def handle_error(self,e):
        logging.error(e)
