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
        try:
            self['token'] = int(token)
        except:
            self['token'] = -1
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
        price = response.css('section#item-details span.item-price > strong::text').get(
            default="").strip()
        self['price'] = clean_number(price)


class SheypoorHomeItem(HomeBaseItem, SheypoorBaseItem):

    def get_production(self, data):
        return {
            "نوساز": datetime.datetime.today().year - 621,
            "۲-۵ سال": datetime.datetime.today().year - 624,
            "2-5 سال": datetime.datetime.today().year - 624,
            "۵-۱۰ سال": datetime.datetime.today().year - 628,
            "5-10 سال": datetime.datetime.today().year - 628,
            "۱۰-۱۵ سال": datetime.datetime.today().year - 633,
            "10-15 سال": datetime.datetime.today().year - 633,
            "۱۵-۲۰ سال": datetime.datetime.today().year - 638,
            "15-20 سال": datetime.datetime.today().year - 638,
            "۲۰ سال به بالا": datetime.datetime.today().year - 644,
        }.get(data, -1)

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
                self['area'] = clean_number(value)
            if 'تعداد اتاق' in key:
                self['room'] = clean_number(value)
            if 'رهن' in key:
                self['deposit'] = clean_number(value)
            if 'اجاره' in key:
                self['rent'] = clean_number(value)
            if 'رهن و اجاره' in key:
                self['swap_deposit_rent'] = True
            if 'نوع کاربری' in key:
                self.clean_sub_category(value)
            elif 'نوع ملک' in key:
                self.clean_sub_category(value)


class SheypoorCarItem(CarBaseItem, SheypoorBaseItem):

    def clean_category(self):
        if 'خودرو' == self['category']:
            self['sub_category'] = 'سواری'

        elif 'موتور سیکلت' == self['category']:
            self['category'] = 'موتورسیکلت و لوازم جانبی'

        elif 'خودرو کلاسیک' == self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'کلاسیک'

        elif 'سنگین و نیمه سنگین' == self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'سنگین'

        elif 'کشاورزی و عمرانی' == self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'سنگین'

        elif 'لوازم و قطعات وسایل نقلیه' == self['category']:
            self['category'] = 'قطعات یدکی و لوازم جانبی خودرو'

        elif 'اجاره خودرو' == self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'اجاره‌ای'

        elif 'سایر وسایل نقلیه' == self['category']:
            pass

    def extract(self, response):
        SheypoorBaseItem.extract(self, response)
        nav = response.css('nav#breadcrumbs ul').xpath('./li')
        brand = nav[len(nav) - 1].xpath('./a/text()').get(default="not-defined").strip()
        if self['category'] not in brand:
            self['brand'] = brand
        self.clean_category()
        tr_list = response.css('section#item-details').xpath('./table/tr')
        for tr in tr_list:
            key = tr.xpath('./th/text()').get().strip()
            value = tr.xpath('./td/text()').get().strip()
            if 'حجم موتور' in key:
                pass
            if 'مدل خودرو' in key:
                self['model'] = value
            if 'نقدی/اقساطی' in key:
                self['cash_installment'] = value
            if 'سال تولید' in key:
                self['production'] = clean_number(value)
            if 'کیلومتر' in key:
                self['consumption'] = clean_number(value)
            if 'رنگ' in key:
                self['color'] = value
            if 'گیربکس' in key:
                self['gear_box'] = value
            if 'نوع سوخت' in key:
                self['fuel'] = value
            if 'وضعیت بدنه' in key:
                self['body_condition'] = value
            if 'نوع شاسی' in key:
                self['chassis_type'] = value


class BamaCarItem(CarBaseItem, BaseItem):

    def create_subject(self, sections):
        subject = ""
        for subject_section in sections:
            if not subject_section == sections[-1]:
                subject += subject_section.strip()
        return subject

    def extract(self, response):
        if self['category'] == 'car':
            self['category'] = 'خودرو'
            self['sub_category'] = 'سواری'
        elif self['category'] == 'motorcycle':
            self['category'] = 'موتورسیکلت و لوازم جانبی'
        url = response.request.url
        self['url'] = url
        self['token'] = clean_number(url.split('-')[1])
        info_right = response.css('div.inforight')
        description = response.css('div.addetaildesc').xpath('./span/text()').get(default="not_defined").strip()
        self['description'] = description
        self['source_id'] = 2
        self['time'] = int(datetime.datetime.now().timestamp())
        title = self.create_subject(info_right.xpath('./div[1]/div[1]/h1[1]/span/text()').getall())
        self['title'] = title
        brand = response.css('div.breadcrumb-div-section ol').xpath('./li[3]/a/span/text()').get(
            default="not_defined").strip()
        self['brand'] = brand
        model = response.css('div.breadcrumb-div-section ol').xpath('./li[4]/a/span/text()').get(
            default="not_defined").strip()
        self['model'] = model
        self['production'] = clean_number(info_right.xpath('./div[1]/div[1]/h1[1]/span/text()').getall()[-1])
        self['thumbnail'] = response.css('a.bamalightgallery-item::attr(href)').get(default="not_defined")
        for detail in info_right.xpath('./p'):
            _class = detail.css('::attr(class)').get()
            if _class == "phone-mobile-block":
                continue
            key = detail.xpath('./span[1]/text()').get().strip()
            if key == "رنگ":
                value = detail.xpath('./span[2]/f[1]/text()').get(default="not_defined").strip()
            elif key == 'محصول':
                value = detail.xpath('./span[2]/a/text()').get(default="not_defined").strip()
            else:
                value = detail.xpath('./span[2]/text()').get(default="not_defined").strip()
            if 'قیمت' in key:
                if 'توضیحات' in value:
                    self['price'] = clean_number(
                        response.css('div.bama-tooltip-and-text').xpath('./div[2]/text()').get(-1).strip())
                else:
                    self['price'] = clean_number(value)
            elif 'شهر' in key:
                self['city'] = value
            elif 'استان' in key:
                self['province'] = value
            elif 'كاركرد' in key:
                self['consumption'] = clean_number(value)
            elif 'رنگ' in key:
                self['color'] = value
            elif 'قسط' in key:
                self['cash_installment'] = 'قسطی'
            elif 'گیربکس' in key:
                self['gear_box'] = value
            elif 'محصول' in key:
                self['company'] = value
            elif 'محله' in key:
                self['neighbourhood'] = value
            elif 'بازديد' in key:
                self['neighbourhood'] = value
            elif 'بدنه' in key:
                self['body_condition'] = value
            elif 'سوخت' in key:
                self['fuel'] = value


class KilidHomeItem(HomeBaseItem, BaseItem):
    deal_type = scrapy.Field()

    def get_production(self, data):
        if data is None:
            return -1
        else:
            return datetime.datetime.today().year - 621 - int(data)

    def get_thumbnail(self, data):
        if data is None:
            return "not_defined"
        elif len(data) > 0:
            return data[0]['pictureUrlSmall']
        else:
            return "not_defined"

    def check_features(self, data):
        if data is None:
            return
        for _dict in data:
            if _dict['nameLat'] == 'balcony':
                self['balcony'] = True
            elif _dict['nameLat'] == 'storage':
                self['storeroom'] = True
            elif _dict['nameLat'] == 'elevator':
                self['elevator'] = True

    def set_category(self, use_type, estate_type):
        if use_type == 'مسکونی':
            self['category'] = f'{"فروش" if self["deal_type"] == "buy" else "اجاره"} مسکونی'
            if estate_type == 'آپارتمان':
                self['sub_category'] = 'آپارتمان'
            elif estate_type == 'ویلایی' or estate_type == 'پنت هاوس' or estate_type == 'برج':
                self['sub_category'] = 'خانه و ویلا'
            elif estate_type == 'زمین/کلنگی':
                self['sub_category'] = 'زمین و کلنگی'
        if use_type == 'اداری' or use_type == 'تجاری' or use_type == 'صنعتی':
            self['category'] = f'{"فروش" if self["deal_type"] == "buy" else "اجاره"} اداری و تجاری'
            if estate_type == 'مغازه':
                self['sub_category'] = 'مغازه و غرفه'
            if estate_type == 'زمین/کلنگی':
                pass
            if estate_type == 'مستغلات':
                pass
            if estate_type == 'باغ/باغچه':
                self['sub_category'] = 'صنعتی،‌ کشاورزی و تجاری'
            if estate_type == 'ویلایی':
                self['sub_category'] = 'دفتر کار، اتاق اداری و مطب'
            if estate_type == 'آپارتمان':
                self['sub_category'] = 'دفتر کار، اتاق اداری و مطب'
            if estate_type == 'کارخانه' or estate_type == 'کارگاه' or estate_type == 'انبار/سوله':
                self['sub_category'] = 'صنعتی،‌ کشاورزی و تجاری'

    def extract(self, data_dict):
        self['token'] = clean_number(data_dict['listingId'] or "")
        self['source_id'] = 3
        self['time'] = int(data_dict['listingDate']/1000 or datetime.datetime.now().timestamp())
        self['title'] = data_dict['title'] or "not_defined"
        self['city'] = data_dict['city'] or "not_defined"
        self['neighbourhood'] = data_dict['neighbourhood'] or "not_defined"
        self['production'] = self.get_production(data_dict['age'])
        self['room'] = int(data_dict['noBeds'] or -1)
        self['area'] = int(data_dict['floorArea'] or -1)
        self['price'] = int(data_dict['price'] or -1)
        self['deposit'] = int(data_dict['deposit'] or -1)
        self['rent'] = int(data_dict['rent'] or -1)
        self['description'] = data_dict['description'] or "not_defined"
        self['thumbnail'] = self.get_thumbnail(data_dict['pictures'])
        self['latitude'] = float(data_dict['latitude'] or -1)
        self['longitude'] = float(data_dict['longitude'] or -1)
        self['parking'] = data_dict['noParkings'] is not None
        self.check_features(data_dict['features'])
        self.set_category(data_dict['landuseType'], data_dict['propertyType'])


def clean_number(data, int_type=True):
    clean_data = "-1"
    for c in str(data):
        if c.isdigit():
            if clean_data == "-1":
                clean_data = ""
            clean_data += c
    if int_type:
        return int(clean_data)
    return clean_data
