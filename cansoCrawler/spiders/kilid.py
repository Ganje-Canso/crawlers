# -*- coding: utf-8 -*-
import json

import scrapy


class KilidSpider(scrapy.Spider):
    name = 'kilid'
    allowed_domains = ['kilid.com', 'kilidstatic.com']
    start_urls = ['https://api.kilid.com/api/location/getAllCities/portal']
    type = "buy"
    page_count = 3

    def parse(self, response):
        city_dict = json.loads(response.body.decode("UTF-8"))
        city_list = city_dict["content"]
        for city in city_list:
            yield response.follow(
                "https://www.kilidstatic.com/kilid-portal-web/information/p_city_{}.json".format(city["locationId"]),
                callback=self.parse_city_sector)

    def parse_city_sector(self, response):
        city_info_dict = json.loads(response.body.decode("UTF-8"))
        location = [{"type": "city", "locationId": city_info_dict["city"][0]["locationId"]}]
        for section_key, section_list in city_info_dict.items():
            if section_key == "city":
                continue
            for section in section_list:
                if len(location) > 1:
                    location.pop()
                location.append({"type": section_key, "locationId": section["locationId"]})
                for category_key, category_value in self.home_type_dict.items():
                    last_sub_category = "sub"
                    body = {"locations": list(location), "subType": self.type, "type": "listing",
                            "sort": "kilid,DESC", "utilityType": category_key, "sub": True}
                    for sub_category in category_value["child"]:
                        body[sub_category["nameLat"]] = body.pop(last_sub_category)
                        last_sub_category = sub_category["nameLat"]
                        # for page_number in range(1, self.page_count):
                        yield scrapy.Request(
                            "https://api.kilid.com/api/listing/search/portal/v2.0?page={}&sort=kilid,DESC".format(
                                1),
                            method='post',
                            body=json.dumps(body), headers={"Content-Type": "application/json"},
                            callback=self.parse_ads,
                            cb_kwargs={"city": city_info_dict["city"][0]["nameFa"],
                                       "neigh": section["nameFa"],
                                       "category": category_value["name"],
                                       "sub_category": sub_category["nameFa"], "page": 1})

    def parse_ads(self, response, city, neigh, category, sub_category, page):
        ads_list = json.loads(response.body.decode("UTF-8"))["content"]
        if len(ads_list) == 0:
            return
        for ad in ads_list:
            if "title" not in ad:
                continue
            yield {
                "page": page,
                "subject": ad["title"],
                "city": city,
                "neigh": neigh,
                "category": category,
                "sub_category": sub_category
            }

    home_type_dict = {
        "residential": {
            "name": "مسکونی",
            "id": 1,
            "child": [
                {
                    "id": 1,
                    "nameLat": "apartment",
                    "nameFa": "آپارتمان"
                },
                {
                    "id": 2,
                    "nameLat": "villa",
                    "nameFa": "ویلایی"
                },
                {
                    "id": 3,
                    "nameLat": "land",
                    "nameFa": "زمین/کلنگی"
                },
                {
                    "id": 18,
                    "nameLat": "pentHouse",
                    "nameFa": "پنت هاوس"
                },
                {
                    "id": 11,
                    "nameLat": "tower",
                    "nameFa": "برج"
                },
                {
                    "id": 12,
                    "nameLat": "swuite",
                    "nameFa": "سوییت"
                },
                {
                    "id": 13,
                    "nameLat": "realEstate",
                    "nameFa": "مستغلات"
                }
            ]
        },
        "commercial": {
            "name": "تجاری",
            "id": 2,
            "child": [
                {
                    "id": 5,
                    "nameLat": "store",
                    "nameFa": "مغازه"
                },
                {
                    "id": 3,
                    "nameLat": "land",
                    "nameFa": "زمین/کلنگی"
                },
                {
                    "id": 13,
                    "nameLat": "realEstate",
                    "nameFa": "مستغلات"
                },
                {
                    "id": 4,
                    "nameLat": "garden",
                    "nameFa": "باغ/باغچه"
                },
                {
                    "id": 2,
                    "nameLat": "villa",
                    "nameFa": "ویلایی"
                }
            ]
        },
        "office": {
            "name": "اداری",
            "id": 3,
            "child": [
                {
                    "id": 1,
                    "nameLat": "apartment",
                    "nameFa": "آپارتمان"
                },
                {
                    "id": 3,
                    "nameLat": "land",
                    "nameFa": "زمین/کلنگی"
                },
                {
                    "id": 13,
                    "nameLat": "realEstate",
                    "nameFa": "مستغلات"
                }
            ]
        },
        "industrial": {
            "name": "صنعتی",
            "id": 4,
            "child": [
                {
                    "id": 15,
                    "nameLat": "factory",
                    "nameFa": "کارخانه"
                },
                {
                    "id": 17,
                    "nameLat": "workshop",
                    "nameFa": "کارگاه"
                },
                {
                    "id": 16,
                    "nameLat": "prpStorage",
                    "nameFa": "انبار/سوله"
                },
                {
                    "id": 13,
                    "nameLat": "realEstate",
                    "nameFa": "مستغلات"
                },
                {
                    "id": 3,
                    "nameLat": "land",
                    "nameFa": "زمین/کلنگی"
                },
                {
                    "id": 4,
                    "nameLat": "garden",
                    "nameFa": "باغ/باغچه"
                }
            ]
        },
    }
