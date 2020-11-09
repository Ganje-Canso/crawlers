# -*- coding: utf-8 -*-
import scrapy

from cansoCrawler.utilities.db_work import get_stop_id, store_stop_id


class EestekhdamSpider(scrapy.Spider):
    name = 'eestekhdam'
    allowed_domains = ['e-estekhdam.com']
    base_url = "https://www.e-estekhdam.com/"
    pages = 10
    stop_id = None
    first_id = None

    def start_requests(self):
        self.stop_id = get_stop_id(self.name, 'recruitment')
        scrapy.Request(url=self.get_page_link(), callback=self.parse)

    def parse(self, response, page=1):
        items_link = response.css('div.media-body a.title::attr(href)').getall()

        for link in items_link:
            if self.get_item_id(link) == self.stop_id:
                self.logger.info(f"stop on:{self.get_item_id(link)} for page:{page}")
                return None

            if page == 1 and self.first_id is None:
                self.first_id = self.get_item_id(link)
                store_stop_id(self.name, 'recruitment', self.get_item_id(link))

            yield response.follow(link, callback=self.parse_item)

        if page < self.pages:
            yield response.follow(self.get_page_link(page + 1), callback=self.parse, cb_kwargs={"page": page + 1})

    def parse_item(self, response):
        pass

    def get_page_link(self, page=1):
        return f"{self.base_url}search?page={page}"

    def get_item_id(self, url):
        return url[url.find('/'): url.find('-')]
