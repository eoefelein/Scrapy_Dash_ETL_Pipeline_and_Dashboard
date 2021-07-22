# -*- coding: utf-8 -*-
import json
import time
from tiny_house_listings.items import TinyHouseListingsItem
import scrapy
from scrapy import Spider
from scrapy.http.request import Request
from scrapy.loader import ItemLoader

# this is where the problem is coming from
"""
helpful explanation?
https://stackoverflow.com/questions/35166821/valueerror-attempted-relative-import-beyond-top-level-package
"""
# from models import *
from scrapy.crawler import CrawlerProcess


class TinyhouselistingsSpider(scrapy.Spider):
    name = "tinyhouselistings"
    listings_url = "https://thl-prod.global.ssl.fastly.net/api/v1/listings/search?area_min=0&measurement_unit=feet&page={}"

    # sends the initial scrapy request to our URL and calls parse
    def start_requests(self):
        page = 1
        yield scrapy.Request(
            url=self.listings_url.format(page), meta={"page": page}, callback=self.parse
        )

    def parse(self, response):
        listings = json.loads(response.body)
        for ad in listings["listings"]:
            item_area = ad["area"]
            item_bathrooms = ad["bathrooms"]
            item_bedrooms = ad["bedrooms"]
            item_city = ad["city"]
            item_createdat = ad["created_at"]
            item_id = ad["id"]
            item_lat = ad["lat"]
            item_lister = ad["lister"]["id"]
            item_lng = ad["lng"]
            item_photo_url = ad["photo_url"]
            item_price = ad["default_price"]["amount_cents"]
            item_property_type = ad["property_type"]
            item_purchase_type = ad["purchase_type"]
            item_slug = ad["slug"]
            item_state = ad["state"]["code"]
            item_status = ad["status"]
            item_title = ad["title"]
            tinyhouselistingsitem = TinyHouseListingsItem(
                area=item_area,
                bathrooms=item_bathrooms,
                bedrooms=item_bedrooms,
                city=item_city,
                createdat=item_createdat,
                id=item_id,
                lat=item_lat,
                lister=item_lister,
                lng=item_lng,
                photo_url=item_photo_url,
                price=item_price,
                propertytype=item_property_type,
                purchasetype=item_purchase_type,
                slug=item_slug,
                state=item_state,
                status=item_status,
                title=item_title,
            )
            # ALL
            yield tinyhouselistingsitem

        page = int(response.meta["page"]) + 1
        if page < int(listings["meta"]["pagination"]["page_count"]):
            yield scrapy.Request(
                url=self.listings_url.format(page),
                meta={"page": page},
                callback=self.parse,
            )
