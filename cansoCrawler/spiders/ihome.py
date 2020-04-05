# -*- coding: utf-8 -*-
import json

import scrapy


class IhomeSpider(scrapy.Spider):
    name = 'ihome'
    allowed_domains = ['ihome.ir']
    start_urls = ['https://scorpion.ihome.ir/v1/search-locations?type=CITY&title=']
    is_sell = 1
    base_url = ""

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
               "locations[]={}&property_type[]={}"
        json_response = json.loads(response.body.decode("UTF-8"))
        neigh_list = json_response["data"]
        for neigh in neigh_list:
            for category in self.home_type_dict["data"].values():
                for sub_category in category["children"]:
                    url = _url.format(self.is_sell, number_of_ads, neigh["path"],
                                      sub_category["slug"])
                    self.logger.info("get %s ads from: %s", number_of_ads, url)
                    yield response.follow(url, callback=self.parse_ads,
                                          cb_kwargs={"city": city, "neigh": neigh["title"],
                                                     "category": category["label"],
                                                     "sub_category": sub_category[
                                                         "label"]})

    def parse_ads(self, response, city, neigh, category, sub_category):
        json_response = json.loads(response.body.decode("UTF-8"))
        ads = json_response["data"]
        for ad in ads:
            yield {
                "subjetc": ad["title"],
                "city": city,
                "neigh": neigh,
                "category": category,
                "sub_category": sub_category,
                "url": response.request.url
            }

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
                        "label": "ویلا",
                        "slug": "residential-vila",
                        "value": "vila"
                    },
                    {
                        "label": "کلنگی",
                        "slug": "residential-dilapidated",
                        "value": "dilapidated"
                    },
                    {
                        "label": "زمین",
                        "slug": "residential-land",
                        "value": "land"
                    },
                    {
                        "label": "برج",
                        "slug": "residential-tower",
                        "value": "tower"
                    },
                    {
                        "label": "مستغلات",
                        "slug": "residential-real_state",
                        "value": "real_state"
                    },
                    {
                        "label": "پنت هاوس",
                        "slug": "residential-penthouse",
                        "value": "penthouse"
                    }
                ]
            },
            "commercial": {
                "label": "تجاری",
                "slug": "commercial",
                "children": [
                    {
                        "label": "اداری",
                        "slug": "commercial-office",
                        "value": "office"
                    },
                    {
                        "label": "مغازه",
                        "slug": "commercial-shop",
                        "value": "shop"
                    },
                    {
                        "label": "زمین تجاری",
                        "slug": "commercial-commercial_land",
                        "value": "commercial_land"
                    },
                    {
                        "label": "باغ",
                        "slug": "commercial-garden",
                        "value": "garden"
                    },
                    {
                        "label": "موقعیت اداری",
                        "slug": "commercial-office_location",
                        "value": "office_location"
                    },
                    {
                        "label": "موقعیت تجاری",
                        "slug": "commercial-business_location",
                        "value": "business_location"
                    }
                ]
            },
            "industrial": {
                "label": "صنعتی",
                "slug": "industrial",
                "children": [
                    {
                        "label": "کارخانه",
                        "slug": "industrial-factory",
                        "value": "factory"
                    },
                    {
                        "label": "کارگاه",
                        "slug": "industrial-workshop",
                        "value": "workshop"
                    },
                    {
                        "label": "انبار صنعتی",
                        "slug": "industrial-warehouse",
                        "value": "warehouse"
                    }
                ]
            }
        }
    }
