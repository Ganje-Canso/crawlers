from cansoCrawler.items.items import BaseItem, HomeBaseItem, CarBaseItem
from cansoCrawler.utilities.uses import hash_token, get_time_stamp, get_production
from cansoCrawler.utilities.Normalize import clean_number


class SheypoorBaseItem(BaseItem):

    def extract_p_d_r(self, price_string):  # extract price deposit rent
        _price_string = price_string.strip()
        if 'رهن' in price_string or 'اجاره' in price_string:
            if 'رهن' in price_string:
                self['deposit'] = clean_number(
                    _price_string[_price_string.find('رهن') + 3: _price_string.find('تومان')])
            if 'اجاره' in price_string:
                self['rent'] = clean_number(
                    _price_string[
                    _price_string.find('اجاره') + 5: _price_string.find('تومان', _price_string.find('اجاره'))])
        else:
            self['price'] = clean_number(_price_string)

    def extract(self, dict_data):
        self['url'] = f"https://www.sheypoor.com/{dict_data['listingID']}"
        self['token'] = hash_token(dict_data['listingID'], 2)
        self['source_id'] = 2
        self['time'] = get_time_stamp()
        self['title'] = dict_data.get('title', 'not_defined')
        self['province'] = dict_data.get('location').get('region', 'not_defined')
        self['city'] = dict_data.get('location').get('city', 'not_defined')
        self['neighbourhood'] = dict_data.get('location').get('neighbourhood', 'not_defined') or 'not_defined'
        self['description'] = dict_data.get('description', 'not_defined')
        images = dict_data.get('images')
        if len(images) > 0:
            self['thumbnail'] = images[0].get('fullSizeURL', images[0].get('thumbnailURL', 'not_defined'))
        self.extract_p_d_r(dict_data.get('priceString', -1))


class SheypoorHomeItem(HomeBaseItem, SheypoorBaseItem):

    def get_production(self, data):
        return {
            "نوساز": get_production(0),
            "۲-۵ سال": get_production(3),
            "2-5 سال": get_production(3),
            "۵-۱۰ سال": get_production(7),
            "5-10 سال": get_production(7),
            "۱۰-۱۵ سال": get_production(12),
            "10-15 سال": get_production(12),
            "۱۵-۲۰ سال": get_production(17),
            "15-20 سال": get_production(17),
            "۲۰ سال به بالا": get_production(23),
        }.get(data, -1)

    def parse_category(self, category, sub_category):
        if 'رهن و اجاره خانه و آپارتمان' in category:
            self['category'] = 'اجاره مسکونی'
            if 'آپارتمان' in sub_category:
                self['sub_category'] = 'آپارتمان'
            elif 'خانه' in sub_category:
                self['sub_category'] = 'خانه و ویلا'
            elif 'ویلا' in sub_category:
                self['sub_category'] = 'خانه و ویلا'

        elif 'خرید و فروش خانه و آپارتمان' in category:
            self['category'] = 'فروش مسکونی'
            if 'آپارتمان' in sub_category:
                self['sub_category'] = 'آپارتمان'
            elif 'خانه و کلنگی' in sub_category:
                self['category'] = 'زمین, کلنگی و باغ'
                self['sub_category'] = 'مسکونی'
            elif 'ویلا' in sub_category:
                self['sub_category'] = 'خانه و ویلا'

        elif 'رهن و اجاره اداری و تجاری' in category:
            self['category'] = 'اجاره اداری و تجاری'
            if 'اداری' in sub_category:
                self['sub_category'] = 'دفتر کار اتاق اداری و مطب'
            elif 'تجاری و مغازه' in sub_category:
                self['sub_category'] = 'مغازه و غرفه'
            elif 'صنعتی (سوله، انبار، کارگاه)' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'
            elif 'دامداری و کشاورزی' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'

        elif 'خرید و فروش اداری و تجاری' in category:
            self['category'] = 'فروش اداری و تجاری'
            if 'اداری' in sub_category:
                self['sub_category'] = 'دفتر کار اتاق اداری و مطب'
            elif 'تجاری و مغازه' in sub_category:
                self['sub_category'] = 'مغازه و غرفه'
            elif 'صنعتی (سوله، انبار، کارگاه)' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'
            elif 'دامداری و کشاورزی' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'

        elif 'زمین و باغ' in category:
            self['category'] = 'زمین, کلنگی و باغ'
            if 'مسکونی' in sub_category:
                self['sub_category'] = 'مسکونی'
            elif 'صنعتی' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'
            elif 'اداری و تجاری' in sub_category:
                self['sub_category'] = 'اداری و تجاری'
            elif 'کشاورزی' in sub_category:
                self['sub_category'] = 'صنعتی, کشاورزی و تجاری'

    def extract_attributes(self, dict_data):
        attribute_list = dict_data['attributes']
        for attribute in attribute_list:
            if attribute.get('attributeLocalyticsKey') == 'age_of_building':
                self['production'] = self.get_production(attribute.get('attributeValue'))

            elif attribute.get('attributeLocalyticsKey') == 'parking':
                self['parking'] = 'دارد' in attribute.get('attributeTitle')

            elif attribute.get('attributeLocalyticsKey') == 'storeroom':
                self['storeroom'] = 'دارد' in attribute.get('attributeTitle')

            elif attribute.get('attributeLocalyticsKey') == 'elevator':
                self['elevator'] = 'دارد' in attribute.get('attributeTitle')

            elif attribute.get('attributeLocalyticsKey') == 'area':
                self['area'] = clean_number(attribute.get('attributeValue'))

            elif attribute.get('attributeLocalyticsKey') == 'numOfRooms':
                self['room'] = clean_number(attribute.get('attributeValue'))

            elif attribute.get('attributeLocalyticsKey') == 'convert_deposit_rent':
                self['swap_deposit_rent'] = True

            elif attribute.get('attributeLocalyticsKey') == 'realEstateType':
                self.parse_category(dict_data['category'].get('c2', 'not_defined') or 'not_defined',
                                    attribute.get('attributeValue'))

    def extract(self, dict_data):
        SheypoorBaseItem.extract(self, dict_data)
        self['advertiser'] = dict_data.get('shopInfo', {}).get('name', 'not_defined')
        self.extract_attributes(dict_data)
        if self['category'] == 'not_defined':
            self.parse_category(dict_data['category'].get('c2', 'not_defined') or 'not_defined', "")


class SheypoorCarItem(CarBaseItem, SheypoorBaseItem):

    def clean_category(self):
        if 'خودرو' == self['category']:
            self['sub_category'] = 'سواری'

        elif 'موتور سیکلت' == self['category']:
            self['category'] = 'موتورسیکلت و لوازم جانبی'
            self['brand'] = 'not_defined'
            self['model'] = 'not_defined'

        elif 'خودرو کلاسیک' == self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'کلاسیک'
            self['brand'] = 'not_defined'
            self['model'] = 'not_defined'

        elif 'سنگین' in self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'سنگین و نیمه سنگین'
            self['brand'] = 'not_defined'
            self['model'] = 'not_defined'

        elif 'کشاورزی و عمرانی' == self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'سنگین و نیمه سنگین'
            self['brand'] = 'not_defined'
            self['model'] = 'not_defined'

        elif 'لوازم و قطعات وسایل نقلیه' == self['category']:
            self['category'] = 'قطعات یدکی و لوازم جانبی خودرو'
            self['brand'] = 'not_defined'
            self['model'] = 'not_defined'

        elif 'اجاره خودرو' == self['category']:
            self['category'] = 'خودرو'
            self['sub_category'] = 'اجاره‌ای'
            self['brand'] = 'not_defined'
            self['model'] = 'not_defined'

        else:
            self['category'] = 'سایر وسایل نقلیه'
            self['brand'] = 'not_defined'
            self['model'] = 'not_defined'

    def extract_attributes(self, attribute_list):
        for attribute in attribute_list:
            if attribute.get('attributeLocalyticsKey') == 'model':
                self['model'] = attribute.get('attributeValue')

            if attribute.get('attributeLocalyticsKey') == 'bodyType':
                self['chassis_type'] = attribute.get('attributeValue')

            if attribute.get('attributeLocalyticsKey') == 'productionYear':
                self['production'] = clean_number(attribute.get('attributeValue'))

            if attribute.get('attributeLocalyticsKey') == 'km':
                self['consumption'] = clean_number(attribute.get('attributeValue'))

            if attribute.get('attributeLocalyticsKey') == 'carColor':
                self['color'] = attribute.get('attributeValue')

            if attribute.get('attributeLocalyticsKey') == 'gearbox':
                self['gear_box'] = attribute.get('attributeValue')

            if attribute.get('attributeLocalyticsKey') == 'carBodyCondition':
                self['body_condition'] = attribute.get('attributeValue')

            if attribute.get('attributeLocalyticsKey') == 'payment_type':
                self['cash_installment'] = attribute.get('attributeValue')

            if attribute.get('attributeLocalyticsKey') == 'fuel':
                self['fuel'] = attribute.get('attributeValue')

    def extract(self, dict_data):
        SheypoorBaseItem.extract(self, dict_data)
        self['brand'] = dict_data['category'].get('c3', 'not_defined') or 'not_defined'
        self.extract_attributes(dict_data['attributes'])
        self['category'] = dict_data['category'].get('c2', 'not_defined') or 'not_defined'
        self.clean_category()
