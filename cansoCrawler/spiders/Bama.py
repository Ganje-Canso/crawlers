# -*- coding: utf-8 -*-
import scrapy

from cansoCrawler.items import BamaCarItem
from cansoCrawler.utilities.db_work import get_last_url
from cansoCrawler.utilities.db_work import get_item_count


class BamaSpider(scrapy.Spider):
    name = 'bama'
    allowed_domains = ['bama.ir']
    _pages = 10  # every 10 minute
    last_url = None
    car_item_count = 0
    motor_item_count = 0

    def start_requests(self):
        url = "https://bama.ir/"
        self.car_item_count = get_item_count('car', 3, f"category = '{'خودرو'}'")
        self.motor_item_count = get_item_count('car', 3, f"category = '{'موتورسیکلت و لوازم جانبی'}'")
        base_url = url + "car/all-brands/all-models/all-trims?page="
        yield scrapy.Request(base_url + "{}".format(1), callback=self.parse,
                             cb_kwargs={"category": "car",
                                        "base_url": base_url})

        base_url = url + "motorcycle?page="
        yield scrapy.Request(base_url + "{}".format(1), callback=self.parse,
                             cb_kwargs={"category": "motorcycle",
                                        "base_url": base_url})

    def parse(self, response, category="", base_url="", page=2):
        # self.logger.info("get ads from page: %s", page - 1)
        url_list = self.get_ad_links(response, category)
        for url in url_list:
            if url == self.get_last_url(category):
                self.logger.info(f"stop on:{url} for page:{page - 1} and category:{category}")
                self.log_stored_items(category)
                return None
            yield from response.follow_all(self.get_ad_links(response, category), callback=self.parse_ad,
                                           cb_kwargs={"category": category})

        # get next page
        if page <= self._pages:
            yield response.follow(base_url + "{}".format(page), callback=self.parse,
                                  cb_kwargs={"page": page + 1, "category": category, "base_url": base_url})
        else:
            self.log_stored_items(category)

    def parse_ad(self, response, category):
        if "detail" not in response.request.url:
            return
        # self.logger.info("get ad from: %s", response.request.url)
        item = BamaCarItem()
        item['category'] = category
        item.extract(response)
        return item

    def get_ad_links(self, response, category):
        if category == "motorcycle":
            _links = response.css('div.eventlist li::attr(onclick)').getall()
            return [link[link.find('http'):len(link) - 1] for link in _links]
        else:
            return response.css('div#adlist li').xpath('./a/@href').getall()

    def get_last_url(self, category):
        if self.last_url is not None:
            return self.last_url
        url = get_last_url('car', 3,
                           f"category = '{'موتورسیکلت و لوازم جانبی' if category == 'motorcycle' else 'خودرو'}'")
        if url is None:
            self.last_url = "not_defined"
        else:
            self.last_url = url
        return self.last_url

    def log_stored_items(self, category):
        new_count = get_item_count('car', 3,
                                   f"category = '{'موتورسیکلت و لوازم جانبی' if category == 'motorcycle' else 'خودرو'}'")
        if new_count is not None and self.car_item_count is not None and self.motor_item_count is not None:
            self.logger.info(f"count of stored items:{new_count - (self.car_item_count if category == 'car' else self.motor_item_count)} for category:{category}")
