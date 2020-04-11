# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import FormRequest


class MelkanaSpider(scrapy.Spider):
    name = 'melkana'
    allowed_domains = ['melkana.com']
    deal_type = 0  # 0 => sell     1 => rent
    page_counter = 3

    def __init__(self, deal_type, **kwargs):
        self.deal_type = 1 if deal_type == "rent" else 0
        super().__init__(**kwargs)

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        url = 'https://www.melkana.com/v3/home/districts/'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        neigh_list = json.loads(response.body.decode('UTF-8'))
        for neigh in neigh_list:
            self.logger.info("get ads for this neigh: %s", neigh["name"])
            for estate_type in self.estate_type_list:
                self.logger.info("get ads for this estate_type: %s", estate_type["name"])
                for estate_document in self.estate_document_list:
                    self.logger.info("get ads for this estate_document: %s", estate_document["name"])
                    for page in range(1, self.page_counter):
                        form_data = self.create_form_data(neigh["marker_latitude"], neigh["marker_longitude"],
                                                          estate_type["id"],
                                                          estate_document["id"], page)
                        headers = {
                            'Accept': 'application/json',
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
                        }
                        yield FormRequest("https://www.melkana.com/v3/home/boundaries", method='POST',
                                          formdata=form_data,
                                          cb_kwargs={"neigh": neigh["name"], "estate_type": estate_type["name"],
                                                     "estate_document": estate_document["name"], "page": page,
                                                     "frm_data": form_data},
                                          callback=self.parse_ads, headers=headers)

    def parse_ads(self, response, neigh, estate_type, estate_document, page, frm_data):
        self.logger.info("gte ads for this form_data: %s", frm_data)
        self.logger.info("get ads for this page: %s", page)
        estate_list = json.loads(response.body.decode('UTF-8'))['estate_list']
        for estate in estate_list:
            yield {
                "subject": estate["title"],
                "neigh": neigh,
                "estate_type": estate_type,
                "estate_document": estate_document,
                "page": page
            }

    def create_form_data(self, lat, lon, estate_type, estate_document, page):
        return {
            "filters[sort][title]": "جدیدترین ها",
            "filters[sort][model]": "approve_time",
            "filters[sort][order]": "desc",
            "filters[deal_type]": str(self.deal_type),
            "filters[deal_type_mobile]": "0",
            "filters[has_tour]": "0",
            "filters[estate_type]": str(estate_type),
            "filters[estate_document]": str(estate_document),
            "filters[price_analyse]": "0",
            "filters[features][0][id]": "1",
            "filters[features][0][name]": "پارکینگ",
            "filters[features][0][title]": "parking",
            "filters[features][0][status]": "false",
            "filters[features][1][id]": "2",
            "filters[features][1][name]": "انباری",
            "filters[features][1][title]": "warehouse",
            "filters[features][1][status]": "false",
            "filters[features][2][id]": "3",
            "filters[features][2][name]": "آسانسور",
            "filters[features][2][title]": "elevator",
            "filters[features][2][status]": "false",
            "filters[features][3][id]": "4",
            "filters[features][3][name]": "بالکن",
            "filters[features][3][title]": "balcony",
            "filters[features][3][status]": "false",
            "filters[center][lat]": str(lat),
            "filters[center][lng]": str(lon),
            "filters[zoom]": "12",
            "filters[foundation][min]": "",
            "filters[foundation][max]": "",
            "filters[foundation][minRange]": "",
            "filters[foundation][maxRange]": "",
            "filters[price_rent][min]": "",
            "filters[price_rent][max]": "",
            "filters[price_rent][minRange]": "",
            "filters[price_rent][maxRange]": "",
            "filters[rahn][min]": "",
            "filters[rahn][max]": "",
            "filters[rahn][minRange]": "",
            "filters[rahn][maxRange]": "",
            "filters[price][min]": "",
            "filters[price][max]": "",
            "filters[price][minRange]": "",
            "filters[price][maxRange]": "",
            "filters[estate_age][min]": "0",
            "filters[estate_age][max]": "40",
            "filters[estate_age][minRange]": "0",
            "filters[estate_age][maxRange]": "40",
            "filters[rooms][min]": "0",
            "filters[rooms][max]": "5",
            "filters[rooms][minRange]": "0",
            "filters[rooms][maxRange]": "5",
            "filters[estate_floor][min]": "-1",
            "filters[estate_floor][max]": "20",
            "filters[estate_floor][minRange]": "-1",
            "filters[estate_floor][maxRange]": "20",
            "filters[building_floors][min]": "1",
            "filters[building_floors][max]": "20",
            "filters[building_floors][minRange]": "1",
            "filters[building_floors][maxRange]": "20",
            "filters[floor_units][min]": "1",
            "filters[floor_units][max]": "10",
            "filters[floor_units][minRange]": "1",
            "filters[floor_units][maxRange]": "10",
            "filters[leftBottom][lat]": str(float(lat) - 0.019429798451156),
            "filters[leftBottom][lng]": str(float(lon) - 0.01656532287597),
            "filters[rightTop][lat]": str(float(lat) + 0.019429798451156),
            "filters[rightTop][lng]": str(float(lon) + 0.01656532287597),
            "filters[polygon]": "",
            "filters[easyFilters]": "",
            "page": str(page)
        }

    estate_type_list = [
        {
            "id": 0,
            "name": "آپارتمان"
        },
        {
            "id": 1,
            "name": "ویلایی"
        }
    ]
    estate_document_list = [
        {
            "id": 0,
            "name": "مسکونی"
        },
        {
            "id": 1,
            "name": "اداری"
        }
    ]
