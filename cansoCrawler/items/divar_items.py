from cansoCrawler.items.items import BaseItem, HomeBaseItem, CarBaseItem, RecruitmentBaseItem
from cansoCrawler.utilities.Normalize import remove_extra_character_and_normalize
from cansoCrawler.utilities.Normalize import convert_alphabetic_number_to_integer
from cansoCrawler.utilities.uses import hash_token, get_time_stamp, extract_model_brand


class DivarBaseItem(BaseItem):
    def extract(self, dict_data):
        self['time'] = get_time_stamp()
        self['title'] = dict_data['data']['share']['title']
        self['description'] = dict_data['widgets']['description']
        self['token'] = hash_token(dict_data['token'], 1)
        self['source_id'] = 1
        self['url'] = dict_data['data']['url']
        image_list = dict_data['widgets']['web_images']
        self['thumbnail'] = (image_list[0][0]['src'].replace('webp', 'jpg')) if len(image_list) > 0 else 'not_defined'
        self['latitude'] = float(dict_data['widgets']['location'].get('latitude', -1))
        self['longitude'] = float(dict_data['widgets']['location'].get('longitude', -1))
        self['neighbourhood'] = dict_data['widgets']['header']['place']


class CarItem(CarBaseItem, DivarBaseItem):

    def extract(self, data):
        DivarBaseItem.extract(self, data)
        list_data = data['widgets']['list_data']
        for i in list_data:
            if i['title'] == 'برند':
                extract_model_brand(self, remove_extra_character_and_normalize(i['value'], check_space=False))
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
            self['category'] = 'قطعات یدکی و لوازم جانبی خودرو'
        elif subcategory == 'موتورسیکلت و لوازم جانبی':
            self['category'] = 'موتورسیکلت و لوازم جانبی'
        elif subcategory == 'قایق و لوازم جانبی':
            self['category'] = 'قایق و لوازم جانبی'
        elif subcategory == 'وسایل نقلیه':
            self['category'] = 'سایر وسایل نقلیه'


class HomeItem(HomeBaseItem, DivarBaseItem):

    def extract(self, data):
        DivarBaseItem.extract(self, data)
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
                self['room'] = convert_alphabetic_number_to_integer(i['value'])
            elif i['title'] == 'متراژ':
                try:
                    self['area'] = int(i['value'].split(' ')[0])
                except:
                    self['area'] = -1
            elif 'قیمت' in i['title'] and 'متر' not in i['title']:
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


class RecruitmentItem(RecruitmentBaseItem, DivarBaseItem):

    def extract(self, dict_data):
        DivarBaseItem.extract(self, dict_data)
