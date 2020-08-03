# -*- coding: utf-8 -*-
import scrapy
import datetime
import json

from cansoCrawler.items import SheypoorHomeItem, SheypoorCarItem

from cansoCrawler.models.utilities import get_last_url


class SheypoorSpider(scrapy.Spider):
    name = 'sheypoor'
    allowed_domains = ['sheypoor.com']
    category = ''
    _pages = 5
    request_time = -1
    last_id = None

    def __init__(self, category='none', **kwargs):
        self.category = category
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(
            url=self.get_url(1),
            callback=self.parse)

    def parse(self, response, page=1):
        json_data = json.loads(response.body.decode('UTF-8'))
        ads = json_data['listings']

        for ad in ads:
            if ad['listingID'] == self.get_last_id():
                self.logger.info(f"stop on:{ad['listingID']} for page:{page}")
                return None
            yield response.follow(url=f"https://www.sheypoor.com/api/v5.3.0/listings/{ad['listingID']}",
                                  callback=self.parse_ad)

        if page <= self._pages:
            yield response.follow(url=self.get_url(page + 1), callback=self.parse, cb_kwargs={"page": page + 1})

    def parse_ad(self, response):
        dict_data = json.loads(response.body.decode('UTF-8'))
        base_category = dict_data['category']["c1"]

        if self.category == 'home' and base_category != 'املاک' or self.category == 'car' and base_category != 'وسایل نقلیه':
            return None

        if self.category == 'home':
            item = SheypoorHomeItem()
            item.extract(dict_data)
            return item
        if self.category == 'car':
            item = SheypoorCarItem()
            item.extract(dict_data)
            return item

        return None

    def get_url(self, page_number):
        request_time = self.get_request_time()
        if self.category == 'home':
            return f"https://www.sheypoor.com/api/v5.3.0/listings?viewId=5&p={page_number}&requestDateTime={request_time}&categoryID=43603&locationType=null&withImage=0"
        else:
            return f"https://www.sheypoor.com/api/v5.3.0/listings?viewId=5&p={page_number}&requestDateTime={request_time}&categoryID=43626&locationType=null&withImage=0"

    def get_request_time(self):
        if self.request_time == -1:
            self.request_time = str(datetime.datetime.now().timestamp())[:15]
        return self.request_time

    def get_last_id(self):
        if self.last_id is not None:
            return self.last_id
        url = get_last_url(self.category, 2)
        if url is None:
            self.last_id = -1
        else:
            urls = url.split('-')
            self.last_id = urls[len(urls) - 1][:-5]
        return self.last_id

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
