# -*- coding: utf-8 -*-
import scrapy
import datetime
import json

from cansoCrawler.items.sheypoor_items import SheypoorHomeItem, SheypoorCarItem
from scrapy import signals

from cansoCrawler.utilities.db_work import get_stop_id, store_stop_id, get_item_count


class SheypoorSpider(scrapy.Spider):
    name = 'sheypoor'
    allowed_domains = ['sheypoor.com']
    category = ''
    _pages = 150
    sheypoor_page = 1
    request_time = -1
    last_id = None
    first_id = "-1"
    item_count = 0

    def __init__(self, category='none', **kwargs):
        self.category = category
        super().__init__(**kwargs)

    def start_requests(self):
        self.item_count = get_item_count(self.category, 2)
        yield scrapy.Request(url=self.get_url(), callback=self.parse, headers=self.headers)

    def parse(self, response, page=1):
        json_data = json.loads(response.body.decode('UTF-8'))
        ads = json_data['listings']

        if len(ads) > 0 and page == 1:
            self.first_id = ads[0]['listingID']

        self.logger.info(f"length of data:{len(ads)} for page:{page} and time is:{self.request_time}")

        for ad in ads:
            if ad['listingID'] == self.get_last_id():
                self.logger.info(f"stop on:{ad['listingID']} for page:{page}")
                return None
            yield response.follow(url=f"https://www.sheypoor.com/api/v5.3.0/listings/{ad['listingID']}",
                                  callback=self.parse_ad, headers=self.headers)

        if page < self._pages:
            yield response.follow(url=self.get_url(), callback=self.parse, cb_kwargs={"page": page + 1},
                                  headers=self.headers)

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

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SheypoorSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        store_stop_id('sheypoor', self.category, self.first_id)
        new_count = get_item_count(self.category, 2)
        if new_count is not None and self.item_count is not None:
            self.logger.info(
                f"count of stored items:{new_count - self.item_count} for category:{self.category}")

    def get_url(self):
        request_time = self.get_request_time()
        if self.category == 'home':
            return f"https://www.sheypoor.com/api/v5.3.0/listings?viewId=5&p={self.sheypoor_page}&requestDateTime={request_time}&categoryID=43603&locationType=null&withImage=0"
        else:
            return f"https://www.sheypoor.com/api/v5.3.0/listings?viewId=5&p={self.sheypoor_page}&requestDateTime={request_time}&categoryID=43626&locationType=null&withImage=0"

    def get_request_time(self):
        if self.request_time == -1 or self.sheypoor_page >= 25:
            self.sheypoor_page = 0
            self.request_time = str(datetime.datetime.now().timestamp())[:15]
        self.sheypoor_page += 1
        return self.request_time

    def get_last_id(self):
        if self.last_id is not None:
            return self.last_id
        url = get_stop_id('sheypoor', self.category)
        if url is None:
            self.last_id = -1
        else:
            self.last_id = url.split('/')[-1]
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

    headers = {
        'Api-Version': 'v5.3.0',
        'App-Version': '5.3.15',
        'User-Agent': 'Android/5.1.1 Sheypoor/5.3.15 VersionCode/5031500 Manufacturer/samsung Model/SM-N950N',
        'Phone-Base': 'true',
        'X-AGENT-TYPE': 'Android App',
        'X-BUILD-MODE': 'Release',
        'X-FLAVOR': 'bazaar',
        'Unique-Id': '49e2bb9c-a7c3-3086-a858-b1e38fbf1fc5'
    }
