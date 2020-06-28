# -*- coding: utf-8 -*-
import scrapy

from cansoCrawler.items import SheypoorHomeItem, SheypoorCarItem


class SheypoorSpider(scrapy.Spider):
    name = 'sheypoor'
    allowed_domains = ['sheypoor.com']
    category = ''
    _pages = 5

    def __init__(self, category='none', **kwargs):
        self.category = category
        super().__init__(**kwargs)

    def start_requests(self):
        if self.category == 'home':
            yield scrapy.Request(url="https://www.sheypoor.com/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86/%D8%A7%D9%85%D9%84%D8%A7%DA%A9", callback=self.parse)
        elif self.category == 'car':
            yield scrapy.Request(url="https://www.sheypoor.com/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86/%D9%88%D8%B3%D8%A7%DB%8C%D9%84-%D9%86%D9%82%D9%84%DB%8C%D9%87", callback=self.parse)

    def parse(self, response):
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
        if page <= self._pages:
            yield response.follow(base_url + "?p={}".format(page), callback=self.parse_ads,
                                  cb_kwargs={"base_url": base_url,
                                             "sub_category": sub_category,
                                             "page": page + 1}
                                  )

    def parse_ad(self, response, sub_category, page):
        nav = " ".join(response.css('nav#breadcrumbs ul').xpath('./li').getall())
        category_list = [
            "املاک",
            "وسایل نقلیه"
            "ورزش فرهنگ فراغت",
            "لوازم الکترونیکی",
            "استخدام",
            "صنعتی، اداری و تجاری",
            "خدمات و کسب و کار",
            "موبایل، تبلت و لوازم",
            "لوازم خانگی",
            "لوازم شخصی",
        ]
        self.logger.info(f"nav: {nav}")
        for category in category_list:
            if category == 'وسایل نقلیه' and self.category == 'car':
                continue
            if category == 'املاک' and self.category == 'home':
                continue
            if category in nav:
                self.logger.info(f"wrong category({category}) for: {response.request.url} | wrong nav: {nav}")
                return None

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
