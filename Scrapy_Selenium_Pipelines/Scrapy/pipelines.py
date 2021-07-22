# -*- coding: utf-8 -*-

# Define your item pipelines here
import psycopg2
import json

# from sqlalchemy.orm import sessionmaker
# from models import TinyHouseListings, db_connect, create_tinyhouselistings_table
# from ...items import TinyHouseListingsItem
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from scrapy.exceptions import NotConfigured
# http://scrapingauthority.com/scrapy-database-pipeline/


class TinyHouseListingsPipeline(object):
    # def __init__(self, db, user, passwd, host):
    #     """
    #     Initializes database connection and sessionmaker.
    #     Creates tinyhouselistings table.
    #     """
    #     engine = db_connect()
    #     create_tinyhouselistings_table(engine)
    #     self.Session = sessionmaker(bind=engine)

    # @classmethod
    # def from_crawler(cls, crawler):
    #     db_settings = crawler.settings.getdict("DB_SETTINGS")
    #     if not db_settings:
    #         raise NotConfigured
    #     db = db_settings["db"]
    #     user = db_settings["user"]
    #     passwd = db_settings["passwd"]
    #     host = db_settings["host"]
    #     return cls(db, user, passwd, host)
    #
    def open_spider(self, spider):
        database = "tiny_house"
        username = "postgres"
        password = "UTData20$"
        hostname = "localhost"
        charset="utf8",
        use_unicode=True,
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password, dbname=database
        )
        # self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        """Save tiny_house_listings to the database.
        Method is called for every item pipeline component.
        """
        self.cur = self.connection.cursor()
        try:
            self.cur.execute(
                "INSERT INTO tiny_house_listings(area, bathrooms, bedrooms, city, createdat, id, lat, lister, lng, photo_url, price, propertytype, purchasetype, slug, state, status, title) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                (
                    item["area"],
                    item["bathrooms"],
                    item["bedrooms"],
                    item["city"],
                    item["createdat"],
                    item["id"],
                    item["lat"],
                    item["lister"],
                    item["lng"],
                    item["photo_url"],
                    item["price"],
                    item["propertytype"],
                    item["purchasetype"],
                    item["slug"],
                    item["state"],
                    item["status"],
                    item["title"],
                    ),
            )
            self.connection.commit()
        except:
            self.connection.rollback()
        return item
        # #old code
        # session = self.Session()
        # deal = TinyHouseListings(**item)

        # try:
        #     session.add(deal)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()

        # return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
