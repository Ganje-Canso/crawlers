# -*- coding: utf-8 -*-
import scrapy
import json

from cansoCrawler.items.iranestekhdam import Item
from cansoCrawler.utilities.db_work import store_stop_id, get_stop_id


class IranestekhdamSpider(scrapy.Spider):
    name = 'iranestekhdam'
    allowed_domains = ['iranestekhdam.ir', 'bazardi.ir']
    base_url = "https://app.bazardi.ir/v1/"
    pages = 20
    first_id = "-1"
    stop_id = None

    def start_requests(self):
        # query items count
        self.stop_id = get_stop_id(self.name, 'recruitment', -1)
        yield scrapy.FormRequest(url=f"{self.base_url}getsearch", formdata=self.get_body(), method='post',
                                 callback=self.parse)

    def parse(self, response, page=1):
        data_dict = json.loads(response.body.decode('UTF-8'))
        if data_dict['success'] == 1:
            ads_list = data_dict['ads']

            if page == 1 and len(ads_list):
                self.logger.info(f"store stopId: {ads_list[0]['id']}")
                store_stop_id(self.name, 'recruitment', ads_list[0]['id'])

            for ad in ads_list:
                if ad['id'] == 0:
                    continue
                if str(ad['id']) == str(self.stop_id):
                    self.logger.info(f"stop on: {ad['id']} for page: {page}")
                    return None
                self.logger.info(f"create item for: {ad['id']}")
                item = Item()
                item.extract(ad)
                yield item

        if page < self.pages:
            yield scrapy.FormRequest(url=f"{self.base_url}getsearch", formdata=self.get_body(page + 1), method='post',
                                     callback=self.parse, cb_kwargs={"page": page + 1})

    def get_body(self, page=1):
        return {
            "page_param": str(page),
            "per_param": "25",
            "type": "list",
        }
