import os
import scrapy
import json

from cansoCrawler.items import DivarHomeItems, DivarCarItems
from cansoCrawler.models.utilities import get_province
from cansoCrawler.utilities.Normalize import normalize_text


class DivarSpider(scrapy.Spider):
    name = "divar"
    start_urls = [
        'https://api.divar.ir/v8/places/cities'
    ]
    allowed_domains = ['divar.ir']


    def __init__(self, category='', **kwargs):
        self.cat = category
        self.category = category
        if self.category == 'home':
            self.category = 'real-estate'
        elif self.category == 'car':
            self.category = 'cars'
        self.metropolis = [
            'تهران',
            'مشهد',
            'کرج',
            'شیراز',
            'اصفهان',
            'اهواز',
            'تبریز',
            'کرمانشاه',
            'قم',
            'رشت'
        ]
        super().__init__(**kwargs)

    def parse(self, response):
        city_list = json.loads(response.body.decode('UTF-8'))["cities"]
        for city in city_list:
            self.logger.info("Getting %s city", city['name'])
            code = city['id']  # City code
            req = {"json_schema": {"category": {"value": self.category}}, "last-post-date": 0}
            yield scrapy.Request(
                f'https://api.divar.ir/v8/search/{code}/{self.category}',
                callback=self.get_page,
                method='POST',
                body=json.dumps(req),
                headers=self.headers,
                cb_kwargs={
                    'city': city,
                    'category': self.category,
                    'counter': 1
                }
            )

    def get_page(self, response, city, category, counter):
        self.logger.info("Getting page {} of {}".format(counter, city["name"]))
        json_response = json.loads(response.body.decode("UTF-8"))
        # Get page details
        for i in range(0, len(json_response['widget_list'])):
            yield scrapy.Request(
                os.path.join(
                    "https://api.divar.ir/v5/posts/",
                    json_response['widget_list'][i]['data']['token']
                ),
                callback=self.get_page_items,
                cb_kwargs={'city': city},
                headers=self.headers
            )
        # Next page
        if (city["name"] not in self.metropolis and counter <= 1) or (city["name"] in self.metropolis and counter <= 2):
            req = {"json_schema": {"category": {"value": category}}, "last-post-date": json_response['last_post_date']}
            yield response.follow(
                f'https://api.divar.ir/v8/search/{city["id"]}/{self.category}',
                callback=self.get_page,
                method='POST',
                body=json.dumps(req),
                cb_kwargs={
                    'city': city,
                    'category': category,
                    'counter': counter + 1
                },
                headers=self.headers
            )

    def get_page_items(self, response, city):
        self.logger.info("Getting page items")
        json_response = json.loads(response.body.decode("UTF-8"))
        if self.category == 'real-estate':
            item = DivarHomeItems()
        elif self.category == 'cars':
            item = DivarCarItems()
        else:
            return
        item.clean(json_response)
        item['city'] = normalize_text(city["name"])
        item['province'] = get_province(item['city'])
        return item

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }
