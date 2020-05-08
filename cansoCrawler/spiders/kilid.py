# -*- coding: utf-8 -*-
import json

import scrapy

from cansoCrawler.items import KilidHomeItem

from cansoCrawler.models.utilities import get_province


class KilidSpider(scrapy.Spider):
    name = 'kilid'
    allowed_domains = ['kilid.com']
    start_urls = ['https://api.kilid.com/api/location/getAllCities/portal']
    _pages = 2

    def parse(self, response):
        city_dict = json.loads(response.body.decode("UTF-8"))
        city_list = city_dict["content"]
        for city in city_list:
            for deal_type in self.deal_type_list:
                body = {"locations": [{"type": "city", "locationId": str(city["locationId"])}], "subType": deal_type,
                        "type": "listing",
                        "sort": "kilid,DESC"}
                for page in range(1, self._pages):
                    yield scrapy.Request(
                        "https://api.kilid.com/api/listing/search/portal/v2.0?page={}&sort=kilid,DESC".format(
                            page),
                        method='post',
                        body=json.dumps(body), headers={"Content-Type": "application/json"},
                        callback=self.parse_ads,
                        cb_kwargs={"deal_type": deal_type})

    def parse_ads(self, response, deal_type):
        ads_list = json.loads(response.body.decode("UTF-8"))["content"]
        if len(ads_list) == 0:
            return
        for ad in ads_list:
            if "id" in ad.keys():
                yield response.follow(url="https://api.kilid.com/api/listing/{}/single/v5".format(ad["id"]),
                                      callback=self.parse_ad, cb_kwargs={"deal_type": deal_type})

    def parse_ad(self, response, deal_type):
        ad = json.loads(response.body.decode('UTF-8'))
        item = KilidHomeItem()
        item['deal_type'] = deal_type
        item['url'] = response.request.url
        item.extract(ad)
        item['province'] = get_province(item['city'])
        return item

    home_type_dict = {
        1: {
            "name": "مسکونی",
            "child": {
                1: {
                    "nameLat": "apartment",
                    "nameFa": "آپارتمان"
                },
                2: {
                    "nameLat": "villa",
                    "nameFa": "ویلایی"
                },
                3: {
                    "nameLat": "land",
                    "nameFa": "زمین/کلنگی"
                },
                18: {
                    "nameLat": "pentHouse",
                    "nameFa": "پنت هاوس"
                },
                11: {
                    "nameLat": "tower",
                    "nameFa": "برج"
                },
                12: {
                    "nameLat": "swuite",
                    "nameFa": "سوییت"
                },
                13: {
                    "nameLat": "realEstate",
                    "nameFa": "مستغلات"
                }
            }
        },
        2: {
            "name": "تجاری",
            "child": {
                5: {
                    "nameLat": "store",
                    "nameFa": "مغازه"
                },
                3: {
                    "nameLat": "land",
                    "nameFa": "زمین/کلنگی"
                },
                13: {
                    "nameLat": "realEstate",
                    "nameFa": "مستغلات"
                },
                4: {
                    "nameLat": "garden",
                    "nameFa": "باغ/باغچه"
                },
                2: {
                    "nameLat": "villa",
                    "nameFa": "ویلایی"
                }
            }
        },
        3: {
            "name": "اداری",
            "child": {
                1: {
                    "nameLat": "apartment",
                    "nameFa": "آپارتمان"
                },
                3: {
                    "nameLat": "land",
                    "nameFa": "زمین/کلنگی"
                },
                13: {
                    "nameLat": "realEstate",
                    "nameFa": "مستغلات"
                }
            }
        },
        4: {
            "name": "صنعتی",
            "child": {
                15: {
                    "nameLat": "factory",
                    "nameFa": "کارخانه"
                },
                17: {
                    "nameLat": "workshop",
                    "nameFa": "کارگاه"
                },
                16: {
                    "nameLat": "prpStorage",
                    "nameFa": "انبار/سوله"
                },
                13: {
                    "nameLat": "realEstate",
                    "nameFa": "مستغلات"
                },
                3: {
                    "nameLat": "land",
                    "nameFa": "زمین/کلنگی"
                },
                4: {
                    "nameLat": "garden",
                    "nameFa": "باغ/باغچه"
                }
            }
        },
    }

    deal_type_list = ['buy', 'rent']
