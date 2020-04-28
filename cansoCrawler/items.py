# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

import datetime


class BaseItem(scrapy.Item):
    token = scrapy.Field()
    source_id = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    neighbourhood = scrapy.Field()
    production = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    thumbnail = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    tell = scrapy.Field()
    swap = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['token'] = -1
        self['source_id'] = -1
        self['time'] = -1
        self['title'] = 'not_defined'
        self['category'] = 'not_defined'
        self['sub_category'] = 'not_defined'
        self['province'] = 'not_defined'
        self['city'] = 'not_defined'
        self['neighbourhood'] = 'not_defined'
        self['production'] = -1
        self['price'] = -1
        self['description'] = 'not_defined'
        self['url'] = 'not_defined'
        self['thumbnail'] = 'not_defined'
        self['latitude'] = -1
        self['longitude'] = -1
        self['tell'] = 'not_defined'
        self['swap'] = False


class HomeBaseItem(scrapy.Item):
    advertiser = scrapy.Field()
    room = scrapy.Field()
    area = scrapy.Field()
    deposit = scrapy.Field()
    rent = scrapy.Field()
    administrative_document = scrapy.Field()
    parking = scrapy.Field()
    elevator = scrapy.Field()
    storeroom = scrapy.Field()
    swap_deposit_rent = scrapy.Field()
    balcony = scrapy.Field()
    estate_floor = scrapy.Field()
    estate_direction = scrapy.Field()
    package = scrapy.Field()
    kitchen = scrapy.Field()
    cooler = scrapy.Field()
    floor_covering = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['advertiser'] = 'not_defined'
        self['room'] = -1
        self['area'] = -1
        self['deposit'] = -1
        self['rent'] = -1
        self['administrative_document'] = False
        self['parking'] = False
        self['elevator'] = False
        self['storeroom'] = False
        self['swap_deposit_rent'] = False
        self['balcony'] = False
        self['cooler'] = False
        self['package'] = False
        self['estate_floor'] = -1
        self['estate_direction'] = 'not_defined'
        self['kitchen'] = 'not_defined'
        self['floor_covering'] = 'not_defined'


class CarBaseItem(scrapy.Item):
    brand = scrapy.Field()
    consumption = scrapy.Field()
    color = scrapy.Field()
    cash_installment = scrapy.Field()
    gear_box = scrapy.Field()
    company = scrapy.Field()
    chassis_type = scrapy.Field()
    model = scrapy.Field()
    body_condition = scrapy.Field()
    fuel = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['brand'] = 'not_defined'
        self['consumption'] = -1
        self['color'] = 'not_defined'
        self['cash_installment'] = 'not_defined'
        self['gear_box'] = 'not_defined'
        self['company'] = 'not_defined'
        self['chassis_type'] = 'not_defined'
        self['model'] = 'not_defined'
        self['body_condition'] = 'not_defined'
        self['fuel'] = 'not_defined'


class SheypoorBaseItem(BaseItem):

    def extract(self, response):
        url = response.request.url
        self['url'] = url
        url_sections = url.split('-')
        dirty_token = url_sections[len(url_sections) - 1]
        token = dirty_token[0:dirty_token.find('.htm')]
        self['token'] = token
        self['source_id'] = 1
        self['time'] = int(datetime.datetime.now().timestamp())
        self['title'] = response.css('section#item-details').xpath(
            './div[1]/h1[1]/text()').get(default="not-defined").strip()
        nav = response.css('nav#breadcrumbs ul').xpath('./li')
        self['province'] = nav[1].xpath('./a/text()').get(default="not-defined").strip()
        self['city'] = nav[2].xpath('./a/text()').get(default="not-defined").strip()
        if len(nav) >= 6:
            self['neighbourhood'] = nav[3].xpath('./a/text()').get(default="not-defined").strip()
        self['description'] = response.css('section#item-details p.description::text').get(
            default="not-defined").strip()
        self['thumbnail'] = response.css('div#item-images img::attr(src)').get(default="not-defined")


class SheypoorHomeItem(HomeBaseItem, SheypoorBaseItem):

    def get_production(self, data):
        return {
            "نوساز": datetime.datetime.today().year - 621,
            "۲-۵ سال": datetime.datetime.today().year - 624,
            "۵-۱۰ سال": datetime.datetime.today().year - 628,
            "۱۰-۱۵ سال": datetime.datetime.today().year - 633,
            "۱۵-۲۰ سال": datetime.datetime.today().year - 638,
            "۲۰ سال به بالا": datetime.datetime.today().year - 644,
        }.get(data)

    def clean_sub_category(self, sub_category):
        if 'رهن و اجاره خانه و آپارتمان' in self['category']:
            self['category'] = 'اجاره مسکونی'
            if 'آپارتمان' in sub_category:
                self['sub_category'] = 'آپارتمان'
            elif 'خانه' in sub_category:
                self['sub_category'] = 'خانه و ویلا'
            elif 'ویلا' in sub_category:
                self['sub_category'] = 'خانه و ویلا'

        elif 'خرید و فروش خانه و آپارتمان' in self['category']:
            self['category'] = 'فروش مسکونی'
            if 'آپارتمان' in sub_category:
                self['sub_category'] = 'آپارتمان'
            elif 'خانه و کلنگی' in sub_category:
                self['sub_category'] = 'زمین و کلنگی'
            elif 'ویلا' in sub_category:
                self['sub_category'] = 'خانه و ویلا'

        elif 'رهن و اجاره اداری و تجاری' in self['category']:
            self['category'] = 'اجاره اداری و تجاری'
            if 'اداری' in sub_category:
                self['sub_category'] = 'دفتر کار اتاق اداری و مطب'
            elif 'تجاری و مغازه' in sub_category:
                self['sub_category'] = 'مغازه و غرفه'
            elif 'صنعتی (سوله، انبار، کارگاه)' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'
            elif 'دامداری و کشاورزی' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'

        elif 'خرید و فروش اداری و تجاری' in self['category']:
            self['category'] = 'فروش اداری و تجاری'
            if 'اداری' in sub_category:
                self['sub_category'] = 'دفتر کار اتاق اداری و مطب'
            elif 'تجاری و مغازه' in sub_category:
                self['sub_category'] = 'مغازه و غرفه'
            elif 'صنعتی (سوله، انبار، کارگاه)' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'
            elif 'دامداری و کشاورزی' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'

        elif 'زمین و باغ' in self['category']:
            self['category'] = 'زمین, کلنگی و باغ'
            if 'مسکونی' in sub_category:
                self['sub_category'] = 'مسکونی'
            elif 'صنعتی' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'
            elif 'اداری و تجاری' in sub_category:
                self['sub_category'] = 'اداری و تجاری'
            elif 'کشاورزی' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'

    def extract(self, response):
        SheypoorBaseItem.extract(self, response)
        tr_list = response.css('section#item-details').xpath('./table/tr')
        for tr in tr_list:
            key = tr.xpath('./th/text()').get().strip()
            value = tr.xpath('./td/text()').get().strip()
            if 'سن بنا' in key:
                self['production'] = self.get_production(value)
            if 'پارکینگ' in key:
                self['parking'] = True
            if 'انباری' in key:
                self['storeroom'] = True
            if 'آسانسور' in key:
                self['elevator'] = True
            if 'متراژ' in key:
                self['area'] = value
            if 'تعداد اتاق' in key:
                self['room'] = value
            if 'رهن' in key:
                self['deposit'] = value
            if 'اجاره' in key:
                self['rent'] = value
            if 'رهن و اجاره' in key:
                self['swap_deposit_rent'] = True
            if 'قیمت' in key:
                self['price'] = value
            if 'نوع کاربری' in key:
                self.clean_sub_category(value)
            elif 'نوع ملک' in key:
                self.clean_sub_category(value)


class SheypoorCarItem(CarBaseItem, SheypoorBaseItem):

    def extract(self, response):
        SheypoorBaseItem.extract(self, response)
        nav = response.css('nav#breadcrumbs ul').xpath('./li')
        self['brand'] = nav[len(nav) - 1].xpath('./a/text()').get(default="not-defined").strip()
        tr_list = response.css('section#item-details').xpath('./table/tr')
        for tr in tr_list:
            key = tr.xpath('./th/text()').get().strip()
            value = tr.xpath('./td/text()').get().strip()
            if 'سال تولید' in key:
                self['production'] = value
            if 'حجم موتور' in key:
                pass
            if 'قیمت' in key:
                self['price'] = value
            if 'مدل خودرو' in key:
                self['model'] = value
            if 'نقدی/اقساطی' in key:
                self['cash_installment'] = value
            if 'سال تولید' in key:
                self['production'] = value
            if 'کیلومتر' in key:
                self['consumption'] = value
            if 'رنگ' in key:
                self['color'] = value
            if 'گیربکس' in key:
                self['gear_box'] = value
            if 'نوع سوخت' in key:
                self['fuel'] = value
            if 'وضعیت بدنه' in key:
                self['cody_condition'] = value
            if 'نوع شاسی' in key:
                self['chassis_type'] = value
