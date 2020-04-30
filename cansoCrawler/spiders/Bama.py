# -*- coding: utf-8 -*-
import scrapy

from cansoCrawler.items import BamaCarItem


class BamaSpider(scrapy.Spider):
    name = 'bama'
    allowed_domains = ['bama.ir']
    _pages = 2

    def start_requests(self):
        url = "https://bama.ir/"

        base_url = url + "car/all-brands/all-models/all-trims?page="
        yield scrapy.Request(base_url + "{}".format(1), callback=self.parse,
                             cb_kwargs={"category": "car",
                                        "base_url": base_url})

        base_url = url + "motorcycle?page="
        yield scrapy.Request(base_url + "{}".format(1), callback=self.parse,
                             cb_kwargs={"category": "motorcycle",
                                        "base_url": base_url})

    def parse(self, response, category, base_url, page=2):
        self.logger.info("get ads from page: %s", page - 1)
        yield from response.follow_all(self.get_ad_links(response, category), callback=self.parse_ad,
                                       cb_kwargs={"category": category})

        # get next page
        if page <= self._pages:
            yield response.follow(base_url + "{}".format(page), callback=self.parse,
                                  cb_kwargs={"page": page + 1})

    def get_ad_links(self, response, category):
        if category == "motorcycle":
            _links = response.css('div.eventlist li::attr(onclick)').getall()
            return [link[link.find('http'):len(link) - 1] for link in _links]
        else:
            return response.css('div#adlist li').xpath('./a/@href').getall()

    def parse_ad(self, response, category):
        if "news" in response.request.url:
            return
        self.logger.info("get ad from: %s", response.request.url)
        item = BamaCarItem()
        item['category'] = category
        item.extract(response)
        return item
