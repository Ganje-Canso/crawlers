# -*- coding: utf-8 -*-
import scrapy

from cansoCrawler.items.items import BamaCarItem
from cansoCrawler.utilities.db_work import get_item_count, store_stop_id, get_stop_id
from scrapy import signals


class BamaSpider(scrapy.Spider):
    name = 'bama'
    allowed_domains = ['bama.ir']
    _pages = 10  # every 10 minute
    car_last_item_id = None
    motor_last_item_id = None
    car_item_count = 0
    motor_item_count = 0
    car_first_item_id = "-1"
    motor_first_item_id = "-1"

    def start_requests(self):
        url = "https://bama.ir/"
        self.car_item_count = get_item_count('car', 3, "category = 'خودرو'")
        self.motor_item_count = get_item_count('car', 3, "category = 'موتورسیکلت و لوازم جانبی'")
        base_url = url + "car/all-brands/all-models/all-trims?page="
        yield scrapy.Request(base_url + "{}".format(1), callback=self.parse,
                             cb_kwargs={"category": "car",
                                        "base_url": base_url})

        base_url = url + "motorcycle?page="
        yield scrapy.Request(base_url + "{}".format(1), callback=self.parse,
                             cb_kwargs={"category": "motorcycle",
                                        "base_url": base_url})

    def parse(self, response, category="", base_url="", page=1):
        url_list = self.get_ad_links(response, category)

        if len(url_list) > 1 and page == 1:
            self.save_first_url(category, url_list[0])

        self.logger.info(f"length of items:{len(url_list)} on page:{page}")

        for url in url_list:
            if url == self.get_last_url(category):
                self.logger.info(f"stop on:{url} for page:{page} and category:{category}")
                return None
            yield response.follow(url=url, callback=self.parse_ad, cb_kwargs={"category": category})

        # get next page
        if page < self._pages:
            yield response.follow(url=base_url + "{}".format(page + 1), callback=self.parse,
                                  cb_kwargs={"page": page + 1, "category": category, "base_url": base_url})

    def parse_ad(self, response, category):
        if "detail" not in response.request.url:
            return
        item = BamaCarItem()
        item['category'] = category
        item.extract(response)
        return item

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BamaSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        self.log_stored_items('motorcycle')
        self.log_stored_items('car')
        store_stop_id('bama', 'motorcycle', self.motor_first_item_id)
        store_stop_id('bama', 'car', self.car_first_item_id)

    def get_ad_links(self, response, category):
        if category == "motorcycle":
            _links = response.css('div.eventlist li::attr(onclick)').getall()
            return [link[link.find('http'):len(link) - 1] for link in _links]
        else:
            return response.css('div#adlist li').xpath('./a/@href').getall()

    def get_last_url(self, category):
        if 'motor' in category:
            if self.motor_last_item_id is not None:
                return self.motor_last_item_id
            url = get_stop_id('bama', 'motorcycle')
            if url is None:
                self.motor_last_item_id = "not_defined"
            else:
                self.motor_last_item_id = url
            return self.motor_last_item_id
        else:
            if self.car_last_item_id is not None:
                return self.car_last_item_id
            url = get_stop_id('bama', 'car')
            if url is None:
                self.car_last_item_id = "not_defined"
            else:
                self.car_last_item_id = url
            return self.car_last_item_id

    def log_stored_items(self, category):
        if 'motor' in category:
            new_count = get_item_count('car', 3, "category = 'موتورسیکلت و لوازم جانبی'")
            if new_count is not None and self.motor_item_count is not None:
                self.logger.info(
                    f"count of stored items:{new_count - self.motor_item_count} for category:{category}")
        else:
            new_count = get_item_count('car', 3, "category = 'خودرو'")
            if new_count is not None and self.car_item_count is not None:
                self.logger.info(
                    f"count of stored items:{new_count - self.car_item_count} for category:{category}")

    def save_first_url(self, category, url):
        if 'motor' in category:
            self.motor_first_item_id = url
        else:
            self.car_first_item_id = url
