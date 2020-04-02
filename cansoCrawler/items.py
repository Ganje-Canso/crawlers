# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SheypoorcrawlerItem(scrapy.Item):
    subject = scrapy.Field()
    price = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
    page = scrapy.Field()

    def clean(self, response):
        nav = response.css('nav#breadcrumbs ul')
        trList = response.css('section#item-details').xpath('./table/tr')
        details = {"empty": False}
        for tr in trList:
            key = tr.xpath('./th/text()').get().strip()
            value = tr.xpath('./td/text()').get().strip()
            details[key] = value

        self['subject'] = response.css('section#item-details').xpath(
            './div[1]/h1[1]/text()').get(default="not-defined").strip()
        self['price'] = response.css('section#item-details span.item-price > strong::text').get(
            default="not-defined").strip()
        self['province'] = nav.xpath('./li[2]/a/text()').get().strip()
        self['city'] = nav.xpath('./li[3]/a/text()').get().strip()
        self['url'] = response.request.url
        self['description'] = response.css('section#item-details p.description::text').get(
            default="not-defined").strip()
        self['details'] = {"empty": True} if len(details) == 1 else details
