import os
import scrapy
import json

from cansoCrawler.items import DivarHomeItems, DivarCarItems
from cansoCrawler.models.utilities import get_province
from cansoCrawler.utilities.Normalize import normalize_text


class DivarSpider(scrapy.Spider):
    name = "divar"
    start_urls = [
        'https://divar.ir/s/tehran'
    ]

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
        self.logger.info("Getting categories and cities from %s", self.start_urls[0])
        cities, categories = self.divar_finder(response)
        for city in cities:
            self.logger.info("Getting %s city", city[0])
            code = city[2]  # City code
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
        self.logger.info("Getting page {} of {}".format(counter, city[0]))
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
        if (city[1] not in self.metropolis and counter <= 1) or (city[1] in self.metropolis and counter <= 2):
            req = {"json_schema": {"category": {"value": category}}, "last-post-date": json_response['last_post_date']}
            yield response.follow(
                f'https://api.divar.ir/v8/search/{city[2]}/{self.category}',
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
        item['city'] = normalize_text(city[1])
        item['province'] = get_province(item['city'])
        return item

    def divar_finder(self, response):
        categories = []  # [name(English)]
        cities = []  # [href, name(Persian), id]

        script = response.xpath("//script")[7].extract()
        script = script[script.find('window.__PRELOADED_STATE__ = "{') + 30:script.find('window.env') - 5]
        script = script.replace('\\', '')
        try:
            script_json = json.loads(script)
        except Exception as e:
            self.logger.error("jsonException: %s", e)
            self.logger.error("json: %s", script)
            return [], []
        places = script_json['city']['places']
        for key in places.keys():
            cities.append([places[key]['slug'], places[key]['name'], str(places[key]['id'])])

        return cities, categories

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }
