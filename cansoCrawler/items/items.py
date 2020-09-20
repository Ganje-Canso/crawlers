# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

from cansoCrawler.utilities.Normalize import clean_number, remove_extra_character_and_normalize

from cansoCrawler.utilities.uses import get_production, get_time_stamp, hash_token, get_persian_year, extract_model_brand


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
        self['swap'] = None


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
        self['administrative_document'] = None
        self['parking'] = None
        self['elevator'] = None
        self['storeroom'] = None
        self['swap_deposit_rent'] = None
        self['balcony'] = None
        self['cooler'] = None
        self['package'] = None
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


class RecruitmentBaseItem(scrapy.Item):
    pass


class BamaCarItem(CarBaseItem, BaseItem):

    def create_subject(self, sections):
        subject = ""
        for subject_section in sections:
            if not subject_section == sections[-1]:
                subject += subject_section.strip() + " "
        return subject.strip()

    def extract(self, response):
        url = response.request.url
        self['url'] = url
        if self['category'] == 'car':
            self['token'] = hash_token(url.split('-')[1], 3)
        else:
            self['token'] = hash_token(url.split('/')[-2].split('-')[-1], 3)
        if self['category'] == 'car':
            self['category'] = 'خودرو'
            self['sub_category'] = 'سواری'
        elif self['category'] == 'motorcycle':
            self['category'] = 'موتورسیکلت و لوازم جانبی'
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
                self['sub_category'] = 'مسکونی'
                self['category'] = 'زمین، کلنگی و باغ'
        if use_type == 'اداری' or use_type == 'تجاری' or use_type == 'صنعتی':
            self['category'] = f'{"فروش" if self["deal_type"] == "buy" else "اجاره"} اداری و تجاری'
            if estate_type == 'مغازه':
                self['sub_category'] = 'مغازه و غرفه'
            elif estate_type == 'زمین/کلنگی':
                self['sub_category'] = 'اداری و تجاری'
                self['category'] = 'زمین، کلنگی و باغ'
            elif estate_type == 'مستغلات':
                self['sub_category'] = 'مستغلات'
            elif estate_type == 'باغ/باغچه':
                self['sub_category'] = 'صنعتی،‌ کشاورزی و تجاری'
            elif estate_type == 'ویلایی':
                self['sub_category'] = 'دفتر کار، اتاق اداری و مطب'
            elif estate_type == 'آپارتمان':
                self['sub_category'] = 'دفتر کار، اتاق اداری و مطب'
            elif estate_type == 'کارخانه' or estate_type == 'کارگاه' or estate_type == 'انبار/سوله':
                self['sub_category'] = 'صنعتی،‌ کشاورزی و تجاری'

    def extract(self, data_dict):
        self['token'] = hash_token(data_dict['listingId'] or "-1", 4)
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
                self['production'] = -1 if primary_dict['value'] is None else get_production(primary_dict['value'])
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

    def check_category(self):
        if "کلنگی" in self["sub_category"]:
            if "مسکونی" in self["category"]:
                self['sub_category'] = 'مسکونی'
                self['category'] = 'زمین، کلنگی و باغ'

    def extract(self, dict_data):
        self['token'] = hash_token(dict_data['code'], 5)
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
        self.check_category()


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
        self['token'] = hash_token(details['code'], 6)
        self['url'] = f"https://www.melkana.com/estate/detail/{details['code']}"
        self['source_id'] = 6
        self['time'] = get_time_stamp()
        self['area'] = int(details['foundation'] or -1)
        self['title'] = self['category'] + " " + (f"{self['area']} متر" if self['area'] != -1 else "")
        self['province'] = 'تهران'
        self['city'] = 'تهران'
        self['production'] = -1 if details['estate_age'] is None else get_production(details['estate_age'])
        self['room'] = int(details['rooms'] or -1)
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

    application_type_dict = {
        '1': 'مسکونی',
        '2': 'اداری و تجاری',
        '3': 'اداری و تجاری',
        '4': 'اداری و تجاری',
        '5': 'سایر املاک',
        '6': 'اداری و تجاری',
        '7': 'زمین کلنگی و باغ',
        '8': 'اداری و تجاری',
        '9': 'سایر املاک',
        '10': 'اداری و تجاری',
        '11': 'اداری و تجاری',
        '12': 'اداری و تجاری'
    }

    def set_category(self, _type, applications):
        application_id = '-1'
        _type = str(_type)
        if len(applications) > 0:
            application_id = str(applications[0]['id'])

        app_name = self.application_type_dict.get(application_id, '')

        if 'سایر' in app_name or 'باغ' in app_name:
            self['category'] = app_name
            return

        self['category'] = self['category'] + app_name

        if 'اداری' in app_name:
            if _type == '1' or _type == '11':
                self['sub_category'] = 'دفتر کار اتاق اداری و مطب'
            if _type == '6' or _type == '8' or _type == '10' or _type == '12' or _type == '13' or _type == '14' or _type == '15' or _type == '16':
                self['sub_category'] = 'صنعتی کشاورزی و تجاری'
            if _type == '4':
                self['sub_category'] = 'مغازه و غرفه'

        if 'مسکونی' in app_name:
            if _type == '1' or _type == '1':
                self['sub_category'] = 'آپارتمان'
            if _type == '2' or _type == '3' or _type == '5' or _type == '11':
                self['sub_category'] = 'خانه و ویلا'
            if _type == '6' or _type == '7':
                self['sub_category'] = 'مسکونی'
                self['category'] = 'زمین، کلنگی و باغ'

    def set_thumbnail(self, files):
        for file in files:
            if file['type'].upper() == 'IMAGE':
                self['thumbnail'] = f"https://file.inpinapp.com/img/200/{file['path']}"
                return
        self['thumbnail'] = 'not_defined'

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
        self['token'] = hash_token(dict_data['id'], 7)
        self['url'] = f"https://www.inpinapp.com/fa/listing/{dict_data['id']}"
        self['source_id'] = 7
        self['area'] = (dict_data['estate'] or {}).get('area', -1) or -1
        self['title'] = self.estate_type_dict.get(
            str(((dict_data['estate'] or {}).get('estate_type') or {}).get('id') or '-1'), "") + " " + \
                        (((dict_data['estate'] or {}).get('region') or {}).get('name', "") or "") + " " + \
                        (f"{self['area']} متر" if self['area'] != -1 else "")

        self['description'] = dict_data['description'] or "not_defined"
        self['neighbourhood'] = ((dict_data['estate'] or {}).get('region') or {}).get('name',
                                                                                      'not_defined') or "not_defined"
        self['production'] = get_production((dict_data['estate'] or {}).get('building_age', -1) or -1)
        self['room'] = ((dict_data['estate'] or {}).get('residential') or {}).get('number_of_bedrooms', -1) or -1
        self['rent'] = dict_data['rent'] or -1
        self['price'] = (dict_data['sale'] or {}).get('total_price', -1) or -1
        self['latitude'] = float(((dict_data['estate'] or {}).get('location') or {}).get('coordinates')[1] or -1)
        self['longitude'] = float(((dict_data['estate'] or {}).get('location') or {}).get('coordinates')[0] or -1)
        self['estate_floor'] = ((dict_data['estate'] or {}).get('residential') or {}).get('floor_number', -1) or -1
        self.set_thumbnail((dict_data['estate'] or {}).get('files', []))
        self.check_property((dict_data['estate'] or {}).get('properties', []))
        self.set_category((dict_data['estate'] or {}).get('estate_type', {}).get('id', '-1'),
                          (dict_data['estate'] or {}).get('applications', []))


class IranpelakCarItem(CarBaseItem, BaseItem):

    def create_title(self):
        result = ""
        if self['brand'] != 'not_defined':
            result += self['brand'] + " "
        if self['model'] != 'not_defined':
            result += self['model'] + " "
        if self['production'] != 'not_defined':
            result += self['production'] + " "
        return result.strip('')

    def extract(self, response):
        self['time'] = get_time_stamp()
        self['source_id'] = 8
        url = response.request.url
        self['token'] = hash_token(url.split('/')[-1], 8)
        self['url'] = url
        self['thumbnail'] = response.css('div[itemprop="image"] img::attr(src)').get('not_defined')
        if 'http' not in self['thumbnail']:
            self['thumbnail'] = f"https://iranpelak.com{self['thumbnail']}"
        self['category'] = 'خودرو'
        self['sub_category'] = 'سواری'
        self['brand'] = response.css('div.header-carname label[itemprop="brand"]::text').get('not_defined').strip()
        self['model'] = response.css('div.header-carname label[itemprop="model"]::text').get('not_defined').strip()
        self['production'] = response.css('div.header-carname label[itemprop="releaseDate"]::text').get(
            'not_defined').strip()
        self['title'] = self.create_title()
        self['production'] = self['production'].replace('(', '')
        self['production'] = int(self['production'].replace(')', '') or -1)
        if self['production'] > get_persian_year():
            self['production'] = self['production'] - 621
        self['gear_box'] = response.css('div.detail-result-icon').css(
            'label[itemprop="vehicleTransmission"]::text').get("not_defined")
        self['consumption'] = clean_number(
            response.css('div.detail-result-icon').css('label[itemprop="value"]::text').get("-1"))
        self['color'] = response.css('div.detail-result-icon').css('label[itemprop="color"]::text').get("not_defined")
        province_city = response.css('div.detail-result-icon label::text').get()
        self['province'] = province_city.split('-')[0] or "not_defined"
        self['city'] = province_city.split('-')[1] or "not_defined"
        self['fuel'] = response.css('label[itemprop="fuelType"]::text').get("not_defined")
        description = response.css('div.search-resualt-tozihat label::text').getall()
        if len(description) == 3:
            self['description'] = description[2]
        elif len(description) == 2:
            self['description'] = description[1]
        else:
            self['description'] = "not_defined"


class HamrahmechanicCarItem(CarBaseItem, BaseItem):
    def extract(self, car_dict):
        self['token'] = hash_token(car_dict['orderId'], 9)
        self['source_id'] = 9
        self['time'] = get_time_stamp()
        self['thumbnail'] = f"https://www.hamrah-mechanic.com{car_dict['imageUrls'][0]}"
        self[
            'url'] = f"https://www.hamrah-mechanic.com/cars-for-sale/{car_dict['carNameEnglish']}/{car_dict['orderId']}/"
        self['title'] = car_dict['carNamePersian'] or "not_defined"
        self['price'] = car_dict['price'] or "not_defined"
        self['consumption'] = car_dict['km'] or "not_defined"
        self['chassis_type'] = car_dict['bodyTypePersian'] or "not_defined"
        self['gear_box'] = car_dict['gearBoxPersian'] or "not_defined"
        self['production'] = car_dict['year'] or "not_defined"
        self['category'] = 'خودرو'
        self['sub_category'] = 'سواری'
        self['tell'] = car_dict.get('consultantPhone', "not_defined")
        self['description'] = car_dict.get('technicalDescription', 'not_defined')
        extract_model_brand(self, remove_extra_character_and_normalize(self['brand'], check_space=False))

