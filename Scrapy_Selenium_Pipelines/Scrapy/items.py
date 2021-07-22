# # -*- coding: utf-8 -*-
from scrapy.item import Item, Field

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TinyHouseListingsItem(scrapy.Item):
    # this should match json being generated
    area = Field()
    bathrooms = Field()
    bedrooms = Field()
    city = Field()
    createdat = Field()
    id = Field()
    lat = Field()
    lister = Field()
    lng = Field()
    photo_url = Field()
    price = Field()
    propertytype = Field()
    purchasetype = Field()
    slug = Field()
    state = Field()
    status = Field()
    title = Field()
    # photo_public_id = Field()
    # photo_urls = Field()
    # photo_public_ids = Field()
    # manager = Field()
