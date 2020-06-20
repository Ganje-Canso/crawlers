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
            self['token'] = hash_token(token)
        except:
            self['token'] = -1
        self['source_id'] = 2
        self['time'] = get_time_stamp()
        self['title'] = response.css('section#item-details').xpath(
            './div[1]/h1[1]/text()').get(default="not_defined").strip()
        nav = response.css('nav#breadcrumbs ul').xpath('./li')
        self['province'] = nav[1].xpath('./a/text()').get(default="not_defined").strip()
        self['city'] = nav[2].xpath('./a/text()').get(default="not_defined").strip()
        if len(nav) >= 6:
            self['neighbourhood'] = nav[3].xpath('./a/text()').get(default="not_defined").strip()
        self['description'] = response.css('section#item-details p.description::text').get(
            default="not_defined").strip()
        self['thumbnail'] = response.css('div#item-images img::attr(src)').get(default="not_defined")
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
        self.clean_sub_category(self['sub_category'])


class SheypoorCarItem(CarBaseItem, SheypoorBaseItem):

    def clean_category(self):
        if 'خودرو' == self['category']:
            self['sub_category'] = 'سواری'

        elif 'موتور سیکلت' == self['category']:
            self['category'] = 'موتورسیکلت و لوازم جانبی'

        elif 'خودرو کلاسیک' == self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'کلاسیک'

        elif 'سنگین' in self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'سنگین و نیمه سنگین'

        elif 'کشاورزی و عمرانی' == self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'سنگین و نیمه سنگین'

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
        brand = nav[len(nav) - 1].xpath('./a/text()').get(default="not_defined").strip()
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
                subject += subject_section.strip() + " "
        return subject.strip()

    def extract(self, response):
        if self['category'] == 'car':
            self['category'] = 'خودرو'
            self['sub_category'] = 'سواری'
        elif self['category'] == 'motorcycle':
            self['category'] = 'موتورسیکلت و لوازم جانبی'
        url = response.request.url
        self['url'] = url
        self['token'] = hash_token(url.split('-')[1])
        info_right = response.css('div.inforight')
        description = response.css('div.addetaildesc').xpath('./span/text()').get(default="not_defined").strip()
        self['description'] = description
        self['source_id'] = 3
        self['time'] = get_time_stamp()
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
        self['token'] = hash_token(data_dict['listingId'] or "-1")
        self['url'] = f"https://kilid.com/{self['deal_type']}/detail/{data_dict['listingId']}"
        self['source_id'] = 4
        self['time'] = get_time_stamp()
        self['title'] = data_dict['title'] or "not_defined"
        self['city'] = data_dict['city'] or "not_defined"
        self['neighbourhood'] = data_dict['neighbourhood'] or "not_defined"
        self['production'] = get_production(data_dict['age'])
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


class IhomeHomeItem(HomeBaseItem, BaseItem):

    def get_img(self, dict_data):
        if 'media' in dict_data:
            if 'images' in dict_data['media']:
                if len(dict_data['media']['images']) > 0:
                    return f"https://media.ihome.ir{dict_data['media']['images'][0]['ls500']['url']}"
        return "not_defined"

    def get_direction(self, list_data):
        data = ""
        for _dict in list_data:
            data += ',' + self.translate_direction(_dict['name'])
        return data

    def translate_direction(self, key):
        return {
            'southern': 'جنوبی',
            'northern': 'شمالی'
        }.get(key, key)

    def get_floor_cover(self, list_data):
        data = ""
        for _dict in list_data:
            data += ',' + self.translate_floor_cover(_dict['name'])
        return data

    def translate_floor_cover(self, key):
        return {
            'ceramic': 'سرامیک'
        }.get(key, key)

    def check_meta(self, dict_data):
        if dict_data['meta'] is None:
            return
        for primary_dict in dict_data['meta']['primary']:
            if primary_dict['key'] == 'completion_year':
                self['production'] = -1 if primary_dict[
                                               'value'] is None else datetime.datetime.today().year - 621 - int(
                    primary_dict['value'])
            if primary_dict['key'] == 'number_of_bedrooms':
                self['room'] = int(primary_dict['value'] or -1)
        for secondary_dict in dict_data['meta']['secondary']:
            if secondary_dict['key'] == 'elevator':
                self['elevator'] = int(secondary_dict['value'] or -1) > 0
            if secondary_dict['key'] == 'storage_areas':
                self['storeroom'] = int(secondary_dict['value'] or -1) > 0
            if secondary_dict['key'] == 'parking_spaces':
                self['parking'] = int(secondary_dict['value'] or -1) > 0
            if secondary_dict['key'] == 'balcony_or_terrace':
                self['balcony'] = int(secondary_dict['value'] or -1) > 0
            if secondary_dict['key'] == 'swap':
                self['swap'] = True
        for other_dict in dict_data['meta']['others']:
            if other_dict['key'] == 'position':
                other_dict['estate_direction '] = self.get_direction(other_dict['values'])
            if other_dict['key'] == 'flooring':
                other_dict['floor_covering '] = self.get_floor_cover(other_dict['values'])

    def extract(self, dict_data):
        self['token'] = hash_token(dict_data['code'])
        self['url'] = f"https://ihome.ir/details-page/{dict_data['code']}"
        self['source_id'] = 5
        self['time'] = get_time_stamp()
        self['title'] = dict_data['title']
        self['advertiser'] = dict_data['agency'].get('name', "not_defined")
        self['area'] = dict_data['area'] or -1
        self['price'] = dict_data['price'] or -1
        self['deposit'] = dict_data['deposit'] or -1
        self['rent'] = dict_data['rent'] or -1
        self['description'] = dict_data['description'] or "not_defined"
        self['thumbnail'] = self.get_img(dict_data)
        self['tell'] = dict_data['agent'].get('mobile', "not_defined")
        self.check_meta(dict_data)


class MelkanaHomeItem(HomeBaseItem, BaseItem):

    def check_features(self, features):
        if 'کولر' in features:
            self['cooler'] = True
        if 'پارکینگ' in features:
            self['parking'] = True
        if 'آسانسور' in features:
            self['elevator'] = True
        if 'انباری' in features:
            self['storeroom'] = True
        if 'بالکن' in features:
            self['balcony'] = True
        if 'پکیج' in features:
            self['package'] = True

    def extract(self, dict_data):
        details = dict_data['details']
        self['token'] = hash_token(details['code'])
        self['url'] = f"https://www.melkana.com/estate/detail/{details['code']}"
        self['source_id'] = 6
        self['time'] = get_time_stamp()
        self['title'] = details['title'] or 'not_defined'
        self['province'] = 'تهران'
        self['city'] = 'تهران'
        self['production'] = -1 if details['estate_age'] is None else datetime.datetime.today().year - 621 - int(
            details['estate_age'])
        self['room'] = int(details['rooms'] or -1)
        self['area'] = int(details['foundation'] or -1)
        if details['deal_type'] == 'فروش':
            self['price'] = clean_number(details['price'])
        else:
            self['deposit'] = clean_number(details['price'])
        self['rent'] = clean_number(details['price_rent'])
        self['description'] = details['description'] or details['features'] or 'not_defined'
        self['thumbnail'] = details['image_360'] or 'not_defined'
        self['latitude'] = dict_data['myLatLng']['lat']
        self['longitude'] = dict_data['myLatLng']['lng']
        self['estate_floor'] = details['estate_floor']
        self['estate_direction'] = details['estate_direction']
        self['kitchen'] = details['kitchen']
        self['floor_covering'] = details['floor_covering']
        self.check_features(details['features'])


class DivarCarItems(CarBaseItem, BaseItem):

    def clean(self, data):
        self['neighbourhood'] = data.get('widgets').get('header').get('place')
        list_data = data['widgets']['list_data']
        for i in list_data:
            if i['title'] == 'برند':
                if 'پراید 111' in i['value']:
                    self['brand'] = 'پراید'
                    self['model'] = '111'
                elif 'پراید 131' in i['value']:
                    self['brand'] = 'پراید'
                    self['model'] = '131'
                elif 'پراید 132' in i['value']:
                    self['brand'] = 'پراید'
                    self['model'] = '132'
                elif 'پراید 141' in i['value']:
                    self['brand'] = 'پراید'
                    self['model'] = '141'
                elif 'پراید اتوماتیک' in i['value']:
                    self['brand'] = 'پراید'
                    self['model'] = 'سایر مدل‌ها'
                elif 'پراید سفری' in i['value']:
                    self['brand'] = 'پراید'
                    self['model'] = 'سایر مدل‌ها'
                elif 'پراید صندوق‌دار' in i['value']:
                    self['brand'] = 'پراید'
                    self['model'] = 'صندوق‌دار'
                elif 'پراید هاچبک' in i['value']:
                    self['brand'] = 'پراید'
                    self['model'] = 'هاچبک'
                elif 'وانت پراید 151' in i['value']:
                    self['brand'] = 'پراید'
                    self['model'] = '151'
                elif 'پراید' in i['value']:
                    self['brand'] = 'پراید'
                    self['model'] = 'سایر مدل‌ها'

                elif 'تیبا صندوق‌دار' in i['value'] or 'تیبا ۱' in i['value']:
                    self['brand'] = 'تیبا'
                    self['model'] = 'صندوق دار'
                elif 'تیبا هاچبک' in i['value'] or 'تیبا ۲' in i['value']:
                    self['brand'] = 'تیبا'
                    self['model'] = 'هاچ بک'
                elif 'تیبا' in i['value']:
                    self['brand'] = 'تیبا'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'آریو اتوماتیک 1600cc' in i['value']:
                    self['brand'] = 'آریو'
                    self['model'] = 'آریو'
                elif 'دنده‌ای 1500cc' in i['value']:
                    self['brand'] = 'آریو'
                    self['model'] = 'آریو'
                elif 'دنده‌ای 1600cc' in i['value']:
                    self['brand'] = 'آریو'
                    self['model'] = 'آریو'
                elif 'آریو' in i['value']:
                    self['brand'] = 'آریو'
                    self['model'] = 'آریو'

                elif 'ساینا اتوماتیک' in i['value']:
                    self['brand'] = 'ساینا'
                    self['model'] = 'اتوماتیک'
                elif 'ساینا دنده‌ای' in i['value']:
                    self['brand'] = 'ساینا'
                    self['model'] = 'دنده ای'
                elif 'ساینا' in i['value']:
                    self['brand'] = 'ساینا'
                    self['model'] = 'سایر مدل‌ها'

                elif 'ام‌وی‌ام 110' in i['value']:
                    self['brand'] = 'ام وی ام'
                    self['model'] = '110'
                elif 'ام‌وی‌ام 110S' in i['value']:
                    self['brand'] = 'ام وی ام'
                    self['model'] = '110S'
                elif 'ام‌وی‌ام 315 صندوق‌دار' in i['value']:
                    self['brand'] = 'ام وی ام'
                    self['model'] = '315 صندوق‌دار'
                elif 'ام‌وی‌ام 315 هاچبک' in i['value']:
                    self['brand'] = 'ام وی ام'
                    self['model'] = '315 هاچبک'
                elif 'ام‌وی‌ام 530' in i['value']:
                    self['brand'] = 'ام وی ام'
                    self['model'] = '530'
                elif 'ام‌وی‌ام 550' in i['value']:
                    self['brand'] = 'ام وی ام'
                    self['model'] = '550'
                elif 'ام‌وی‌ام X33' in i['value']:
                    self['brand'] = 'ام وی ام'
                    self['model'] = 'X33'
                elif 'ام‌وی‌ام X22' in i['value']:
                    self['brand'] = 'ام وی ام'
                    self['model'] = 'X22'
                elif 'ام‌وی‌ام X33 S' in i['value']:
                    self['brand'] = 'ام وی ام'
                    self['model'] = 'X33 S'
                elif 'ام‌وی‌ام' in i['value']:
                    self['brand'] = 'ام وی ام'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'پژو 2008' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '2008'
                elif 'پژو 205' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '205'
                elif 'پژو 206' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '206'
                elif 'پژو 206 SD' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '206 SD'
                elif 'پژو 207i' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '207i'
                elif 'پژو 207i SD' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '207i SD'
                elif 'پژو 301' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '301'
                elif 'پژو 404' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '404'
                elif 'پژو 405' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '405'
                elif 'پژو 406' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '406'
                elif 'پژو 407' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '407'
                elif 'پژو 504' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '504'
                elif 'پژو 508' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '508'
                elif 'پژو پارس' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = 'پارس'
                elif 'پژو پارس لیموزین' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = 'پارس لیموزین'
                elif 'پژو روآ' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = 'روآ'
                elif 'پژو روآ سال' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = 'روآ'
                elif 'پژو RD' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = 'RD'
                elif 'پژو RDI' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = 'RDI'
                elif 'پژو' in i['value']:
                    self['brand'] = 'پژو'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'پیکان بنزینی' in i['value'] or 'پیکان دوگانه‌ سوز CNG' in i['value'] or 'پیکان دوگانه‌ سوز LPG' in \
                        i['value']:
                    self['brand'] = 'پیکان'
                    self['model'] = 'سواری'
                elif 'پیکان وانت' in i['value']:
                    self['brand'] = 'پیکان'
                    self['model'] = 'وانت'
                elif 'پیکان' in i['value']:
                    self['brand'] = 'پیکان'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'دنا پلاس' in i['value']:
                    self['brand'] = 'دنا'
                    self['model'] = 'پلاس'
                elif 'دنا معمولی' in i['value']:
                    self['brand'] = 'دنا'
                    self['model'] = 'معمولی'
                elif 'دنا' in i['value']:
                    self['brand'] = 'دنا'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'رانا EL' in i['value']:
                    self['brand'] = 'رانا'
                    self['model'] = 'رانا EL'
                elif 'رانا LX' in i['value']:
                    self['brand'] = 'رانا'
                    self['model'] = 'رانا LX'
                elif 'رانا' in i['value']:
                    self['brand'] = 'رانا'
                    self['model'] = 'رانا (‌سایر مدل‌ها)'

                elif 'سمند سریر' in i['value']:
                    self['brand'] = 'سمند'
                    self['model'] = 'سریر'
                elif 'سمند سورن' in i['value']:
                    self['brand'] = 'سمند'
                    self['model'] = 'سورن'
                elif 'سمند EL' in i['value']:
                    self['brand'] = 'سمند'
                    self['model'] = 'EL'
                elif 'سمند LX' in i['value']:
                    self['brand'] = 'سمند'
                    self['model'] = 'LX'
                elif 'سمند SE' in i['value']:
                    self['brand'] = 'سمند'
                    self['model'] = 'SE'
                elif 'سمند X7' in i['value']:
                    self['brand'] = 'سمند'
                    self['model'] = 'X7'
                elif 'سمند' in i['value']:
                    self['brand'] = 'سمند'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'وانت آریسان آریسان' in i['value']:
                    self['brand'] = 'آریسان'
                    self['model'] = 'وانت'
                elif 'وانت آریسان' in i['value']:
                    self['brand'] = 'آریسان'
                    self['model'] = 'وانت'

                elif 'هایما S5' in i['value']:
                    self['brand'] = 'هایما'
                    self['model'] = 'هایما S5'
                elif 'هایما S7' in i['value']:
                    self['brand'] = 'هایما'
                    self['model'] = 'هایما S7'
                elif 'هایما' in i['value']:
                    self['brand'] = 'هایما'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'جک J3 سدان' in i['value']:
                    self['brand'] = 'جک'
                    self['model'] = 'J3 سدان'
                elif 'جک J3 هاچبک' in i['value']:
                    self['brand'] = 'جک'
                    self['model'] = 'J3 هاچبک'
                elif 'جک J4' in i['value']:
                    self['brand'] = 'جک'
                    self['model'] = 'J4'
                elif 'جک J5' in i['value']:
                    self['brand'] = 'جک'
                    self['model'] = 'J5'
                elif 'جک S3' in i['value']:
                    self['brand'] = 'جک'
                    self['model'] = 'S3'
                elif 'جک S5' in i['value']:
                    self['brand'] = 'جک'
                    self['model'] = 'S5'
                elif 'جک' in i['value']:
                    self['brand'] = 'جک'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'جیلی Emgrand 7' in i['value']:
                    self['brand'] = 'جیلی'
                    self['model'] = 'Emgrand 7'
                elif 'جیلی Emgrand 7_RV' in i['value']:
                    self['brand'] = 'جیلی'
                    self['model'] = 'Emgrand 7_RV'
                elif 'جیلی Emgrand X7' in i['value']:
                    self['brand'] = 'جیلی'
                    self['model'] = 'Emgrand X7'
                elif 'جیلی GC6' in i['value']:
                    self['brand'] = 'جیلی'
                    self['model'] = 'GC6'
                elif 'جیلی' in i['value']:
                    self['brand'] = 'جیلی'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'لیفان 520' in i['value']:
                    self['brand'] = 'لیفان'
                    self['model'] = 'لیفان 520'
                elif 'لیفان 520i' in i['value']:
                    self['brand'] = 'لیفان'
                    self['model'] = 'لیفان 520i'
                elif 'لیفان 620' in i['value']:
                    self['brand'] = 'لیفان'
                    self['model'] = 'لیفان 620'
                elif 'لیفان 820' in i['value']:
                    self['brand'] = 'لیفان'
                    self['model'] = 'لیفان 820'
                elif 'لیفان X50' in i['value']:
                    self['brand'] = 'لیفان'
                    self['model'] = 'لیفان X50'
                elif 'لیفان X60' in i['value']:
                    self['brand'] = 'لیفان'
                    self['model'] = 'لیفان X60'
                elif 'لیفان' in i['value']:
                    self['brand'] = 'لیفان'
                    self['model'] = 'سایر مدل‌ها'

                elif 'رنو 21' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = '21'
                elif 'رنو 5' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = '5'
                elif 'رنو 5 مونتاژ' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = '5 مونتاژ'
                elif 'رنو اسکالا' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'اسکالا'
                elif 'رنو پارس تندر' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'پارس تندر'
                elif 'رنو پی کی' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'پی کی'
                elif 'رنو تلیسمان' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'تلیسمان'
                elif 'رنو تندر 90' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'تندر 90'
                elif 'رنو تندر 90 پلاس' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = '  تندر 90 پلاس'
                elif 'رنو داستر' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'داستر'
                elif 'رنو ساندرو' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'ساندرو'
                elif 'رنو ساندرو استپ‌وی' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'ساندرو استپ وی'
                elif 'رنو سپند' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'سپند'
                elif 'رنو سفران' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'سفران'
                elif 'رنو سیمبل' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'سیمبل'
                elif 'رنو فلوئنس' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'فلوئنس'
                elif 'رنو کپچر' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'کپچر'
                elif 'رنو کوليوس' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'کوليوس'
                elif 'رنو لاگونا' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'لاگونا'
                elif 'رنو لتیتود' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'لتیتود'
                elif 'رنو مگان' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'مگان'
                elif 'رنو مگان مونتاژ' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'مگان مونتاژ'
                elif 'وانت رنو وانت تندر 91' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = 'وانت رنو وانت تندر 90'
                elif 'رنو' in i['value']:
                    self['brand'] = 'رنو'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'برلیانس کراس' in i['value']:
                    self['brand'] = 'برلیانس'
                    self['model'] = 'کراس'
                elif 'برلیانس H220' in i['value']:
                    self['brand'] = 'برلیانس'
                    self['model'] = 'H220'
                elif 'برلیانس H230' in i['value']:
                    self['brand'] = 'برلیانس'
                    self['model'] = 'H230'
                elif 'برلیانس H320' in i['value']:
                    self['brand'] = 'برلیانس'
                    self['model'] = 'H320'
                elif 'برلیانس H330' in i['value']:
                    self['brand'] = 'برلیانس'
                    self['model'] = 'H330'
                elif 'برلیانس V5' in i['value']:
                    self['brand'] = 'برلیانس'
                    self['model'] = 'V5'
                elif 'برلیانس' in i['value']:
                    self['brand'] = 'برلیانس'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'هیوندای آزرا گرنجور' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'آزرا گرنجور'
                elif 'هیوندای آوانته' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'آوانته'
                elif 'هیوندای اسکوپ' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'اسکوپ'
                elif 'هیوندای اکسل' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'اکسل'
                elif 'هیوندای اکسنت' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'اکسنت'
                elif 'هیوندای اکسنت مونتاژ' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'اکسنت مونتاژ'
                elif 'هیوندای النترا' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'النترا'
                elif 'هیوندای النترا مونتاژ' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'النترا مونتاژ'
                elif 'هیوندای تراجت' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'تراجت'
                elif 'هیوندای توسان ix 35' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'توسان ix 34'
                elif 'هیوندای جنسیس سدان' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'جنسیس سدان'
                elif 'هیوندای جنسیس کوپه' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'جنسیس کوپه'
                elif 'هیوندای سانتافه ix 45' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'سانتافه ix 44'
                elif 'هیوندای سنتنیال' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'سنتنیال'
                elif 'هیوندای سوناتا LF' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'سوناتا LF'
                elif 'هیوندای سوناتا LF هیبرید' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'سوناتا LF هیبرید'
                elif 'هیوندای سوناتا NF' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = '‌سایر مدل‌ها'
                elif 'هیوندای سوناتا YF' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = '‌سایر مدل‌ها'
                elif 'هیوندای سوناتا YF' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = '‌سایر مدل‌ها'
                elif 'هیوندای وراکروز ix55' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'وراکروز ix54‌'
                elif 'هیوندای ورنا' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'ورنا'
                elif 'هیوندای ولستر' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'ولستر'
                elif 'هیوندای FX کوپه' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'FX کوپه'
                elif 'هیوندای i10 مونتاژ' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'i10 مونتاژ'
                elif 'هیوندای i20' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'i20'
                elif 'هیوندای i30' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'i30'
                elif 'هیوندای i40' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'i40'
                elif 'هیوندای i40 استیشن' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = 'i40 استیشن'
                elif 'هیوندای' in i['value']:
                    self['brand'] = 'هیوندای'
                    self['model'] = '‌سایر مدل‌ها'

                elif 'کیا اپتیما' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'اپتیما'
                elif 'کیا اپیروس' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'اپیروس'
                elif 'کیا اسپورتیج' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'اسپورتیج'
                elif 'کیا پیکانتو' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'پیکانتو'
                elif 'کیا ریو' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'ریو'
                elif 'کیا ریو مونتاژ' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'ریو مونتاژ'
                elif 'کیا سراتو' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'سراتو'
                elif 'کیا سراتو کوپه' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'سراتو کوپه'
                elif 'کیا سراتو مونتاژ' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'سراتو مونتاژ'
                elif 'کیا سورنتو' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'سورنتو'
                elif 'کیا سول' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'سول'
                elif 'کیا کادنزا' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'کادنزا'
                elif 'کیا کارناوال' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'کارناوال'
                elif 'کیا کارنز' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'کارنز'
                elif 'کیا موهاوی' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = 'موهاوی'
                elif 'کیا' in i['value']:
                    self['brand'] = 'کیا'
                    self['model'] = '‌سایر مدل‌ها'
            elif i['title'] == 'کارکرد':
                try:
                    self['consumption'] = int(i['value'].replace('٫', '').strip())
                except:
                    self['consumption'] = -1
            elif i['title'] == 'سال ساخت':
                try:
                    self['production'] = int(i['value'][-4:])
                except:
                    self['production'] = -1
            elif i['title'] == 'رنگ':
                self['color'] = i['value']
            elif i['title'] == 'قیمت':
                try:
                    self['price'] = int(i['value'].replace('تومان', '').strip().replace('٫', ''))
                except:
                    self['price'] = -1
            elif i['title'] == 'نوع آگهی':
                pass
            elif i['title'] == 'مایلم معاوضه کنم':
                self['swap'] = True if i['value'] == 'هستم' else False
            elif i['title'] == 'گیربکس':
                self['gear_box'] = i['value']
            elif i['title'] == 'وضعیت بدنه':
                self['body_condition'] = i['value']

        self['time'] = get_time_stamp()
        self['title'] = data['data']['share']['title']
        self['description'] = data['widgets']['description']
        self['token'] = hash_token(data['token'])
        self['source_id'] = 1
        self['url'] = data['data']['url']
        self['thumbnail'] = data['data']['seo'].get('thumbnail', 'not_defined')
        if self['thumbnail'] is not None and isinstance(self['thumbnail'], list):
            self['thumbnail'] = self['thumbnail'][0] if 'http' in self['thumbnail'][0] else 'not_defined'
        self['latitude'] = float(data['widgets']['location'].get('latitude', -1))
        self['longitude'] = float(data['widgets']['location'].get('longitude', -1))
        subcategory = data['data']['category']['title']
        if subcategory == 'سنگین':
            self['sub_category'] = 'سنگین و نیمه سنگین'
            self['category'] = 'خودرو'
        elif subcategory == 'خودرو':
            self['sub_category'] = 'وسایل نقلیه'
            self['category'] = 'خودرو'
        elif subcategory == 'سواری' or subcategory == 'اجاره‌ای' or subcategory == 'کلاسیک':
            self['category'] = 'خودرو'
            self['sub_category'] = subcategory
        elif subcategory == 'قطعات یدکی و لوازم جانبی خودرو':
            self['category'] = 'قطعات یدکی و لوازم جانبی وسایل نقلیه'
        elif subcategory == 'موتورسیکلت و لوازم جانبی':
            self['category'] = 'موتورسیکلت و لوازم جانبی'
        elif subcategory == 'قایق و لوازم جانبی':
            self['category'] = 'قایق و لوازم جانبی'
        elif subcategory == 'وسایل نقلیه':
            self['category'] = 'سایر وسایل نقلیه'


class DivarHomeItems(HomeBaseItem, BaseItem):

    def clean(self, data):

        for i in data['widgets']['list_data']:
            if i['title'] == 'دسته‌بندی':
                subcat = i['value']
                if subcat == 'اجاره مسکونی (آپارتمان، خانه، زمین)':
                    self['category'] = 'اجاره مسکونی'
                    self['sub_category'] = 'سایر املاک'
                elif subcat == 'فروش مسکونی (آپارتمان، خانه، زمین)':
                    self['category'] = 'فروش مسکونی'
                    self['sub_category'] = 'سایر املاک'
                elif subcat == 'فروش اداری و تجاری (مغازه، دفتر کار، صنعتی)':
                    self['category'] = 'فروش اداری و تجاری'
                    self['sub_category'] = 'سایر املاک'
                elif subcat == 'اجاره اداری و تجاری (مغازه، دفتر کار، صنعتی)':
                    self['category'] = 'اجاره اداری و تجاری'
                    self['sub_category'] = 'سایر املاک'
                elif subcat == 'خدمات املاک':
                    self['category'] = 'خدمات املاک'
                    self['sub_category'] = 'سایر املاک'
                elif subcat == 'زمین و کلنگی':
                    self['sub_category'] = 'مسکونی'
                    self['category'] = 'زمین، کلنگی و باغ'
                else:
                    self['sub_category'] = subcat
            elif i['title'] == 'سال ساخت':
                try:
                    self['production'] = int(i['value'])
                except:
                    data['production'] = -1
            elif i['title'] == 'تعداد اتاق':
                self['room'] = clean_number(i['value'])
            elif i['title'] == 'متراژ':
                try:
                    self['area'] = int(i['value'].split(' ')[0])
                except:
                    self['area'] = -1
            elif 'قیمت' in i['title']:
                try:
                    self['price'] = int(i['value'].replace('تومان', '').strip().replace('٫', ''))
                except:
                    self['price'] = -1
            elif i['title'] == 'ودیعه':
                try:
                    self['deposit'] = int(i['value'].replace('تومان', '').strip().replace('٫', ''))
                except Exception as e:
                    self['deposit'] = 0
            elif i['title'] == 'اجاره':
                try:
                    self['rent'] = int(i['value'].replace('تومان', '').strip().replace('٫', ''))
                except:
                    if ['value'] == 'مجانی':
                        self['rent'] = 0
                    elif ['value'] == 'توافقی':
                        self['rent'] = -1
            elif i['title'] == 'نوع آگهی':
                adtype = i['value']
                if adtype == 'ارائه':
                    pass
                elif adtype == 'فروشی':
                    pass
            elif i['title'] == 'آگهی‌دهنده':
                self['advertiser'] = i['value']
            elif i['title'] == 'سند اداری':
                self['administrative_document'] = False if i['value'] == 'نیست' else True
            elif i['title'] == 'مایلم معاوضه کنم':
                self['swap'] = True if i['value'] == 'هستم' else False

        self['time'] = get_time_stamp()
        self['title'] = data['data']['share']['title']
        self['description'] = data['widgets']['description']
        self['token'] = hash_token(data['token'])
        self['source_id'] = 1
        self['url'] = data['data']['url']
        self['thumbnail'] = data['data']['seo'].get('thumbnail', 'not_defined')
        if self['thumbnail'] is not None and isinstance(self['thumbnail'], list):
            self['thumbnail'] = self['thumbnail'][0] if 'http' in self['thumbnail'][0] else 'not_defined'
        self['latitude'] = float(data['widgets']['location'].get('latitude', -1))
        self['longitude'] = float(data['widgets']['location'].get('longitude', -1))
        self['neighbourhood'] = data['widgets']['header']['place']
        category = data['data']['category']['slug']
        if category == 'apartment-rent' or category == 'house-villa-rent':
            self['category'] = 'اجاره مسکونی'
        elif category == 'house-villa-sell' or category == 'apartment-sell':
            self['category'] = 'فروش مسکونی'
        elif category == 'industry-agriculture-business-sell':
            self['category'] = 'فروش اداری و تجاری'
        elif category == 'shop-sell':
            self['category'] = 'فروش اداری و تجاری'
        elif category == 'office-sell':
            self['category'] = 'فروش اداری و تجاری'
        elif category == 'industry-agriculture-business-rent':
            self['category'] = 'اجاره اداری و تجاری'
        elif category == 'shop-rent':
            self['category'] = 'اجاره اداری و تجاری'
        elif category == 'office-rent':
            self['category'] = 'اجاره اداری و تجاری'
        elif category == 'agency':
            self['category'] = 'خدمات املاک'
        elif category == 'partnership':
            self['category'] = 'خدمات املاک'
        elif category == 'financial-legal':
            self['category'] = 'خدمات املاک'
        elif category == 'presell':
            self['category'] = 'خدمات املاک'
        elif category == 'املاک':
            self['category'] = 'سایر املاک'
            self['sub_category'] = 'سایر املاک'


class InpinHomeItem(HomeBaseItem, BaseItem):
    estate_type_dict = {
        '1': 'آپارتمان',
        '2': 'ویلا',
        '3': 'باغ ویلا',
        '4': 'مغازه',
        '5': 'پنت هاس',
        '6': 'زمین',
        '7': 'کلنگی',
        '8': 'باغ باغچه',
        '9': 'مستغلات',
        '10': 'کارخانه',
        '11': 'سوییت',
        '12': 'دامداری',
        '13': 'انبار',
        '14': 'سوله',
        '15': 'استودیو',
        '16': 'سالن تالار',
    }

    def set_thumbnail(self, files):
        for file in files:
            if file['type'].upper() == 'IMAGE':
                self['thumbnail'] = f"https://file.inpinapp.com/img/200/{file['path']}"
                break

    def check_property(self, properties):
        for property in properties:
            if 'parking' in property['title'].lower():
                self['parking'] = (property['pivot']['number'] or -1) > 0
            if 'elevator' in property['title'].lower():
                self['elevator'] = (property['pivot']['number'] or -1) > 0
            if 'warehouse' in property['title'].lower():
                self['storeroom'] = True
            if 'balcony' in property['title'].lower():
                self['balcony'] = True
            if 'FLOORING_TYPE' in property['category'].upper():
                if 'ceramic' in property['title'].lower():
                    self['floor_covering'] = 'سرامیک'
                if 'stone' in property['title'].lower():
                    self['floor_covering'] = 'سنگ'
                if 'mosaic' in property['title'].lower():
                    self['floor_covering'] = 'موزائیک'
                if 'carpet' in property['title'].lower():
                    self['floor_covering'] = 'موکت'
            if 'cooler' in property['title'].lower():
                self['cooler'] = True
            if 'package' in property['title'].lower():
                self['package'] = True
            if 'CABINET_TYPE' in property['category'].upper():
                self['kitchen'] = property['title'].lower()
            if 'GEOGRAPHICAL_DIRECTION' in property['category'].upper():
                if 'north' in property['title'].lower():
                    self['estate_direction'] = 'شمالی'
                if 'south' in property['title'].lower():
                    self['estate_direction'] = 'جنوبی'
                if 'west' in property['title'].lower():
                    self['estate_direction'] = 'غربی'
                if 'east' in property['title'].lower():
                    self['estate_direction'] = 'شرقی'

    def extract(self, dict_data):
        self['time'] = get_time_stamp()
        self['token'] = hash_token(dict_data['id'])
        self['url'] = f"https://www.inpinapp.com/fa/ad/{dict_data['id']}"
        self['source_id'] = 7
        self['title'] = self.estate_type_dict.get(
            str(((dict_data['estate'] or {}).get('estate_type') or {}).get('id') or -1), "") + " " + \
                        ((dict_data['estate'] or {}).get('region') or {}).get('name', "") or ""
        self['description'] = dict_data['description'] or "not_defined"
        self['neighbourhood'] = ((dict_data['estate'] or {}).get('region') or {}).get('name',
                                                                                      'not_defined') or "not_defined"
        self['area'] = (dict_data['estate'] or {}).get('area', -1) or -1
        self['production'] = (dict_data['estate'] or {}).get('building_age', -1) or -1
        self['room'] = ((dict_data['estate'] or {}).get('residential') or {}).get('number_of_bedrooms', -1) or -1
        self['rent'] = dict_data['rent'] or -1
        self['price'] = (dict_data['sale'] or {}).get('total_price', -1) or -1
        self['latitude'] = float(((dict_data['estate'] or {}).get('location') or {}).get('coordinates')[1] or -1)
        self['longitude'] = float(((dict_data['estate'] or {}).get('location') or {}).get('coordinates')[0] or -1)
        self['estate_floor'] = ((dict_data['estate'] or {}).get('residential') or {}).get('floor_number', -1) or -1
        self.set_thumbnail((dict_data['estate'] or {}).get('files', []))
        self.check_property((dict_data['estate'] or {}).get('properties', []))


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


def hash_token(token):
    import hashlib
    return int(str(int(hashlib.sha1(str(token).encode()).hexdigest(), 16))[:18])


def get_time_stamp():
    return int(datetime.datetime.now().timestamp())


def get_production(age):
    if age is None:
        return -1
    else:
        return datetime.datetime.today().year - 621 - int(age)
