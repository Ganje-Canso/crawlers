# -*- coding: utf-8 -*-
import json

import scrapy

from cansoCrawler.items.items import IhomeHomeItem

from cansoCrawler.utilities.db_work import get_province


class IhomeSpider(scrapy.Spider):
    name = 'ihome'
    allowed_domains = ['ihome.ir']
    start_urls = ['https://scorpion.ihome.ir/v1/search-locations?type=CITY&title=']
    base_url = ""
    _pages = 2

    def parse(self, response):
        json_response = json.loads(response.body.decode("UTF-8"))
        city_list = json_response["data"]
        for city in city_list:
            self.logger.info("get neigh for %s city", city["location_slug"])
            yield response.follow(
                "https://scorpion.ihome.ir/v1/search-locations?title=&parent_id={}&type=DISTRICT_SUB_DISTRICT".format(
                    city["id"]),
                callback=self.parse_neighbourhood,
                cb_kwargs={"city": city["title"]})

    def parse_neighbourhood(self, response, city):
        number_of_ads = 10
        _url = "https://scorpion.ihome.ir/v1/flatted-properties?is_sale={}&source=website&paginate={}&" \
               "locations[]={}&property_type[]={}&page={}"
        json_response = json.loads(response.body.decode("UTF-8"))
        neigh_list = json_response["data"]
        for neigh in neigh_list:
            for category in self.home_type_dict["data"].values():
                for sub_category in category["children"]:
                    for is_sale in [1, 0]:
                        for page in range(1, self._pages):
                            url = _url.format(is_sale, number_of_ads, neigh["path"],
                                              sub_category["slug"], page)
                            self.logger.info("get %s ads from: %s", number_of_ads, url)
                            yield response.follow(url, callback=self.parse_ads,
                                                  cb_kwargs={"city": city, "neigh": neigh["title"],
                                                             "category": category["label"],
                                                             "sub_category": sub_category[
                                                                 "label"], 'is_sale': is_sale})

    def parse_ads(self, response, city, neigh, category, sub_category, is_sale):
        json_response = json.loads(response.body.decode("UTF-8"))
        ads = json_response["data"]
        for ad in ads:
            item = IhomeHomeItem()

            item["neighbourhood"] = neigh
            item["category"] = ('فروش ' if is_sale == 1 else "اجاره ") + category
            item["sub_category"] = sub_category
            item.extract(ad)

            province_city = get_province(city)
            item['province'] = province_city["p"]
            item["city"] = province_city["c"]

            return item

    home_type_dict = {
        "data": {
            "residential": {
                "label": "مسکونی",
                "slug": "residential",
                "children": [
                    {
                        "label": "آپارتمان",
                        "slug": "residential-apartment",
                        "value": "apartment"
                    },
                    {
                        "label": "خانه و ویلا",
                        "slug": "residential-vila",
                        "value": "vila"
                    },
                    {
                        "label": "زمین و کلنگی",
                        "slug": "residential-dilapidated",
                        "value": "dilapidated"
                    },
                    {
                        "label": "زمین و کلنگی",
                        "slug": "residential-land",
                        "value": "land"
                    },
                    {
                        "label": "خانه و ویلا",
                        "slug": "residential-tower",
                        "value": "tower"
                    },
                    {
                        "label": "آپارتمان",
                        "slug": "residential-real_state",
                        "value": "real_state"
                    },
                    {
                        "label": "خانه و ویلا",
                        "slug": "residential-penthouse",
                        "value": "penthouse"
                    }
                ]
            },
            "commercial": {
                "label": "اداری و تجاری",
                "slug": "commercial",
                "children": [
                    {
                        "label": "دفتر کار، اتاق اداری و مطب",
                        "slug": "commercial-office",
                        "value": "office"
                    },
                    {
                        "label": "مغازه و غرفه",
                        "slug": "commercial-shop",
                        "value": "shop"
                    },
                    {
                        "label": "صنعتی،‌ کشاورزی و تجاری",
                        "slug": "commercial-commercial_land",
                        "value": "commercial_land"
                    },
                    {
                        "label": "صنعتی،‌ کشاورزی و تجاری",
                        "slug": "commercial-garden",
                        "value": "garden"
                    },
                    {
                        "label": "دفتر کار، اتاق اداری و مطب",
                        "slug": "commercial-office_location",
                        "value": "office_location"
                    },
                    {
                        "label": "صنعتی،‌ کشاورزی و تجاری",
                        "slug": "commercial-business_location",
                        "value": "business_location"
                    }
                ]
            },
            "industrial": {
                "label": "اداری و تجاری",
                "slug": "industrial",
                "children": [
                    {
                        "label": "صنعتی،‌ کشاورزی و تجاری",
                        "slug": "industrial-factory",
                        "value": "factory"
                    },
                    {
                        "label": "صنعتی،‌ کشاورزی و تجاری",
                        "slug": "industrial-workshop",
                        "value": "workshop"
                    },
                    {
                        "label": "صنعتی،‌ کشاورزی و تجاری",
                        "slug": "industrial-warehouse",
                        "value": "warehouse"
                    }
                ]
            }
        }
    }
