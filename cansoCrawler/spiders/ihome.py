# -*- coding: utf-8 -*-
import json

import scrapy


class IhomeSpider(scrapy.Spider):
    name = 'ihome'
    allowed_domains = ['ihome.ir']
    start_urls = ['https://scorpion.ihome.ir/v1/search-locations?type=CITY&title=']
    transaction_type = "sell"
    base_url = ""

    def parse(self, response):
        json_response = json.loads(response.body.decode("UTF-8"))
        city_list = json_response["data"]
        for city in city_list:
            yield response.follow(
                "https://scorpion.ihome.ir/v1/search-locations?title=&parent_id={}&type=DISTRICT_SUB_DISTRICT".format(
                    city["id"]),
                callback=self.parse_neighbourhood,
                cb_kwargs={"city": city["title"], "url_part2": city["location_slug"]})

    def parse_neighbourhood(self, response, city, url_part2):
        json_response = json.loads(response.body.decode("UTF-8"))
        neigh_list = json_response["data"]
        for neigh in neigh_list:
            for category in self.home_type_dict["data"].values():
                for sub_category in category["children"]:
                    yield response.follow(
                        "https://ihome.ir/{}-{}/{}/{}".format(self.transaction_type, sub_category["slug"], url_part2,
                                                              neigh["location_slug"]),
                        callback=self.parse_ads, cb_kwargs={"city": city, "neigh": neigh["title"],
                                                            "category": category["label"],
                                                            "sub_category": sub_category[
                                                                "label"]})

    def parse_ads(self, response, city, neigh, category, sub_category):
        links = response.css('div#result-row').xpath('./div/a/@href')
        yield from response.follow_all(links, callback=self.parse_ad, cb_kwargs={"city": city, "neigh": neigh,
                                                                                 "category": category,
                                                                                 "sub_category": sub_category})

    def parse_ad(self, response, city, neigh, category, sub_category):
        details = {"empty": False}
        self.set_first_details(response, details)
        self.set_primary_details(response, details)
        self.set_extend_details(response, details)
        yield {
            "subject": response.css('h1.property-detail_title::text').get('not-defined').strip(),
            "price": self.get_price(response),
            "city": city,
            "neigh": neigh,
            "category": category,
            "sub_category": sub_category,
            "url": response.request.url,
            "description": response.css('div.property-detail_agency-box_description p::text').get(
                'not-defined').strip(),
            "details": details
        }

    def get_price(self, response):
        price = ""
        _price = response.css('div.property-detail_price-box').xpath('./div[2]')
        price += _price.xpath('./strong[1]/text()').get().strip()
        price += _price.xpath('./text()')[0].get().strip()
        price += _price.xpath('./strong[2]/text()').get().strip()
        price += _price.xpath('./text()')[1].get().strip()

        return price

    def set_first_details(self, response, details):
        first_details = response.css('div.property-detail__icons')[0]
        first_details_values = first_details.css('span.property-detail__icons-item__value span::text').getall()
        first_details_keys = first_details.css('span.property-detail__icons-item__unit::text').getall()
        for key, value in dict(zip(first_details_keys, first_details_values)):
            if len(key.strip()) != 0 and len(value.strip()) != 0:
                details[key] = value

    def set_primary_details(self, response, details):
        primary_details = response.css('div.properties__list')
        for primary_detail in primary_details:
            key = primary_detail.xpath('./small/text()').get().strip()
            value = primary_detail.xpath('./span/text()').get().strip()
            details[key] = value

    def set_extend_details(self, response, details):
        extend_details = response.css('div.list__grid__item')
        for extend_detail in extend_details:
            key = extend_detail.xpath('./small/text()').get().strip()
            value = extend_detail.xpath('./span/text()').get().strip() + extend_detail.xpath('./span/small/text()').get(
                '').strip
            details[key] = value

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
