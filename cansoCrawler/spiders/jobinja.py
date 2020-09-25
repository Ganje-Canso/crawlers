# -*- coding: utf-8 -*-
import scrapy

from cansoCrawler.utilities.db_work import store_stop_id, get_stop_id


class JobinjaSpider(scrapy.Spider):
    name = 'jobinja'
    allowed_domains = ['jobinja.ir']

    pages = 100
    first_id = None
    stop_id = None

    def start_requests(self):
        self.stop_id = get_stop_id(self.name, 'recruitment', 'noting')
        yield scrapy.Request(self.get_url(), callback=self.parse)

    def parse(self, response, page=1):
        items_link = response.css('a.c-jobListView__titleLink::attr(href)').getall()

        for link in items_link:

            if self.stop_id == self.get_item_id(link):
                self.logger.info(f"stop on: {self.get_item_id(link)} for page: {page}, url: {link}")
                return None

            yield response.follow(link, callback=self.parse_item, cb_kwargs={"page": page})

        if page < self.pages:
            yield response.follow(self.get_url(page + 1), callback=self.parse, cb_kwargs={"page": page + 1})

    def parse_item(self, response, page):
        url = response.url

        if page == 1 and self.first_id is None:
            self.first_id = self.get_item_id(url)
            store_stop_id(self.name, 'recruitment', self.first_id)

        extra_data = {}
        info_li_list = response.css('ul.c-infoBox').xpath('./li')
        for li in info_li_list:
            key = li.xpath('./h4[1]/text()').get().strip()
            value = li.xpath('./div[1]').xpath('string(.)').get().strip()
            extra_data[key] = value

        # TODO متن معرفی شرکت

        yield {
            "id": self.get_item_id(url),
            "url": url,
            "page": page,
            "title": response.css('div.c-jobView__titleText::text').get().strip(),
            "description": response.css('div.s-jobDesc').xpath('string(.)').get().strip(),
            "extra_data": extra_data
        }

    def get_url(self, page=1):
        return f"https://jobinja.ir/jobs?page={page}"

    def get_item_id(self, url):
        return url[url.find('jobs/') + 5: url.find('/', url.find('jobs/') + 5)]
