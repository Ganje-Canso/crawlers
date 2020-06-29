# -*- coding: utf-8 -*-
import scrapy
import json

from cansoCrawler.items import HamrahmechanicCarItem

from cansoCrawler.models.utilities import get_province


class HamrahmechanicSpider(scrapy.Spider):
    name = 'hamrahmechanic'
    allowed_domains = ['www.hamrah-mechanic.com']
    url = 'https://www.hamrah-mechanic.com/api/exhibition/'
    _pages = 6

    def start_requests(self):
        for page in range(1, self._pages):
            yield scrapy.Request(url=self.url, body=json.dumps(self.get_body(page)), headers=self.headers,
                                 callback=self.parse,
                                 method='post')

    def parse(self, response):
        json_response = json.loads(response.body.decode('UTF-8'))
        if json_response['success']:
            car_list = json_response['data']['list']
            for car in car_list:
                item = HamrahmechanicCarItem()
                item.extract(car)
                item['city'] = car['cityNamePersian']
                item['province'] = get_province(car['cityNamePersian'] or 'noting')
                yield item
        else:
            self.logger.info(f"empty: {json_response}")

    def get_body(self, page):
        return {"Brands": [], "BrandsEnglishName": [], "Models": [], "ModelsEnglishName": [], "BodyTypes": [],
                "BodyTypesEnglishName": [], "Cities": [], "CitiesEnglishName": [], "Gearboxes": [],
                "GearboxesEnglishName": [], "Km": 250000, "MiladyRange": "", "ShamsyRange": "", "Page": page,
                "Size": 20, "PriceFrom": 0, "PriceTo": 5000, "SearchText": "", "Sort": 2, "GreatDeal": 0}

    headers = {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }
