# -*- coding: utf-8 -*-
import scrapy

from cansoCrawler.items import SheypoorHomeItem, SheypoorCarItem


class SheypoorSpider(scrapy.Spider):
    name = 'sheypoor'
    allowed_domains = ['sheypoor.com']
    start_urls = ['https://sheypoor.com/']
    category = ''

    def __init__(self, category='none', **kwargs):
        self.category = category
        super().__init__(**kwargs)

    def parse(self, response):
        self.logger.info('get categories from: %s', self.start_urls[0])
        liList = response.css('div#categories-card li.card')
        for i in range(10):
            if i < 4:
                category_url = liList[i].xpath('./div[1]/a/@href').get().strip()
                category = liList[i].xpath('./div[1]/a/span[2]/text()').get().strip()
            else:
                category = liList[i].xpath('./a/div/text()').get().strip(' ')
                category_url = liList[i].xpath('./a/@href').get().strip(' ')

            if category == self.translate_category():
                yield response.follow(category_url,
                                      callback=self.parse_sub_category)
                break

    def parse_sub_category(self, response):
        self.logger.info('get sub_categories for: %s', self.category)
        liList = response.css('section#categories').xpath('./div/ul/li')
        for li in liList:
            sub_category = li.css('span.title::text').get().strip()
            sub_category_url = li.css('a::attr(href)').get().strip()
            yield response.follow(sub_category_url,
                                  callback=self.parse_ads,
                                  cb_kwargs={"sub_category": sub_category,
                                             "base_url": sub_category_url})

    def parse_ads(self, response, base_url, sub_category, page=2):
        self.logger.info("get ads from page: %s", page - 1)
        yield from response.follow_all(response.xpath('//article/div[2]/h2/a/@href').getall(),
                                       callback=self.parse_ad,
                                       cb_kwargs={"sub_category": sub_category,
                                                  "page": page - 1})

        # get next page
        if page <= 1:
            yield response.follow(base_url + "?p={}".format(page), callback=self.parse_ads,
                                  cb_kwargs={"base_url": base_url,
                                             "sub_category": sub_category,
                                             "page": page + 1}
                                  )

    def parse_ad(self, response, sub_category, page):
        if self.category == 'home':
            item = SheypoorHomeItem()
            item['category'] = sub_category
            item.extract(response)
            return item
        if self.category == 'car':
            item = SheypoorCarItem()
            item['category'] = sub_category
            item.extract(response)
            return item

        return None

    def translate_category(self):
        return {
            "home": "املاک",
            "car": "وسایل نقلیه",
            "sport": "ورزش فرهنگ فراغت",
            "electronic": "لوازم الکترونیکی",
            "job": "استخدام",
            "industry": "صنعتی، اداری و تجاری",
            "service": "خدمات و کسب و کار",
            "mobile": "موبایل، تبلت و لوازم",
            "home_appliance": "لوازم خانگی",
            "personal": "لوازم شخصی",
        }.get(self.category, "none")
