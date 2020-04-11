# -*- coding: utf-8 -*-
import json

import scrapy


class KilidSpider(scrapy.Spider):
    name = 'kilid'
    allowed_domains = ['kilid.com']
    start_urls = ['https://api.kilid.com/api/location/getAllCities/portal']
    deal_type = "buy"
    page_count = 3

    def __init__(self, deal_type='buy', **kwargs):
        if deal_type == "rent":
            self.deal_type = "rent"
        else:
            self.deal_type = "buy"
        super().__init__(**kwargs)

    def parse(self, response):
        city_dict = json.loads(response.body.decode("UTF-8"))
        city_list = city_dict["content"]
        for city in city_list:
            body = {"locations": [{"type": "city", "locationId": str(city["locationId"])}], "subType": self.deal_type,
                    "type": "listing",
                    "sort": "kilid,DESC"}
            for page in range(1, self.page_count):
                yield scrapy.Request(
                    "https://api.kilid.com/api/listing/search/portal/v2.0?page={}&sort=kilid,DESC".format(
                        page),
                    method='post',
                    body=json.dumps(body), headers={"Content-Type": "application/json"},
                    callback=self.parse_ads,
                    cb_kwargs={"page": page})

    def parse_ads(self, response, page):
        ads_list = json.loads(response.body.decode("UTF-8"))["content"]
        if len(ads_list) == 0:
            return
        for ad in ads_list:
            if "id" in ad.keys():
                yield response.follow(url="https://api.kilid.com/api/listing/{}/single/v5".format(ad["id"]),
                                      callback=self.parse_ad, cb_kwargs={"page": page})

    def parse_ad(self, response, page):
        ad = json.loads(response.body.decode('UTF-8'))
        yield {
            "id": ad["listingId"],
            "subject": ad["title"],
            "page": page,
            "rent": ad["rent"],
            "deposit": ad["deposit"],
            "price": ad["price"],
            "deal_type": self.deal_type
        }

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
