import sqlite3

from hazm import Normalizer


def normalize_item(item, ad_type):
    if 'home' == ad_type:
        normalize_home_item(item)
    elif 'car' == ad_type:
        normalize_car_item(item)
    item['category'] = remove_extra_character_and_normalize(item['category'])
    item['sub_category'] = remove_extra_character_and_normalize(item['sub_category'])


def normalize_home_item(item):
    item['kitchen'] = normalize_kitchen(item['kitchen'])
    item['floor_covering'] = normalize_floor_covering(item['floor_covering'])
    item['advertiser'] = remove_extra_character_and_normalize(item['advertiser'])


def normalize_kitchen(kitchen):
    kitchen = remove_extra_character_and_normalize(kitchen)
    if ('mdf' in kitchen or 'MDF' in kitchen or 'ام دی اف' in kitchen) and \
            ('open' in kitchen or 'OPEN' in kitchen or 'اوپن' in kitchen):
        return 'اوپن ام دی اف'
    if 'mdf' in kitchen or 'MDF' in kitchen or 'ام دی اف' in kitchen:
        return 'کابینت ام دی اف'
    if 'چوب' in kitchen or 'چوبی' in kitchen:
        return 'کابینت چوبی'
    if 'فلز' in kitchen or 'فلزی' in kitchen:
        return 'کابینت فلزی'
    if 'هایگلاس' in kitchen or 'هایگلس' in kitchen or 'higlass' in kitchen:
        return 'کابینت هایگلاس'
    if 'ممبران' in kitchen or 'membrane' in kitchen:
        return 'کابینت ممبران'
    return 'not_defined'


def normalize_floor_covering(floor_covering):
    floor_covering = remove_extra_character_and_normalize(floor_covering)
    if 'پارکت' in floor_covering:
        return 'پارکت'
    if 'سرامیک' in floor_covering or 'سرامیك' in floor_covering:
        return 'سرامیک'
    if 'سنگ' in floor_covering:
        return 'سنگ'
    if 'لمینت' in floor_covering or 'لمینیت' in floor_covering:
        return 'لمینیت'
    if 'موزاییک' in floor_covering or 'موزائیک' in floor_covering or 'موزاییك' in floor_covering or 'موزائیك' in floor_covering:
        return 'موزائیک'
    if 'موکت' in floor_covering:
        return 'موکت'
    return 'not_defined'


def normalize_car_item(item):
    item['brand'] = normalize_brand(item['brand'])
    item['model'] = normalize_model(item['model'], item['brand'])
    item['color'] = normalize_color(item['color'])
    item['cash_installment'] = normalize_cash_installment(item['cash_installment'])
    item['gear_box'] = remove_extra_character_and_normalize(item['gear_box'])
    item['company'] = remove_extra_character_and_normalize(item['company'])
    item['chassis_type'] = normalize_chassis_type(item['chassis_type'])
    item['body_condition'] = remove_extra_character_and_normalize(item['body_condition'])
    item['fuel'] = normalize_fuel(item['fuel'])


def normalize_model(model, brand):
    model = remove_extra_character_and_normalize(model)
    model = model.upper()
    model = model.replace('هاچبک', 'هاچ بک')
    model = model.replace('هاچبك', 'هاچ بک')
    model = model.replace('هاچ بك', 'هاچ بک')
    model = model.replace('مونتاژ', '')
    model = model.strip()

    if 'سایر مدل ها' in model:
        return 'not_defined'
    if 'وانت' == model and 'وانت' == brand:
        return 'not_defined'
    if 'وانت' in model and 'وانت' == brand:
        return model.replace('وانت', '').strip()
    if 'سایر' in model:
        return 'not_defined'
    if 'آریسان' in model or 'اریسان' in model:
        return 'آریسان'
    if 'X33S' in model:
        return 'X33 S'
    if 'CLA' in model and 'بنز' in brand:
        return 'کلاس CLA'
    if 'CLS' in model and 'بنز' in brand:
        return 'کلاس CLS'
    if 'C' in model and 'بنز' in brand:
        return 'کلاس C'
    if 'E' in model and 'بنز' in brand:
        return 'کلاس E'
    if 'SL' in model and 'بنز' in brand:
        return 'کلاس SL'
    if 'S' in model and 'بنز' in brand:
        return 'کلاس S'
    if 'GLK' in model and 'بنز' in brand:
        return 'کلاس GLK'
    if 'ML' in model and 'بنز' in brand:
        return 'کلاس ML'
    if 'کوپه' in model and ('کروک' in model or 'کروك' in model):
        return 'not_defined'
    if 'صبا' in model and 'پراید' in brand:
        return 'صندوق دار'
    if '151' in model and 'پراید' in brand:
        return 'وانت'
    if 'نسیم' in model and 'پراید' in brand:
        return 'هاچ بک'
    if '206' in model and 'پژو' in brand:
        return '206'
    if '405' in model and 'پژو' in brand:
        return '405'
    if '207' in model and 'پژو' in brand:
        return '207'
    if 'پارس' in model and 'پژو' in brand:
        return 'پارس'
    if ('روا' in model or 'روآ' in model or 'آردی' in model or 'اردی' in model or 'RD' in model) and 'پژو' in brand:
        return 'آردی'
    if ('سواری' in model or 'سدان' in model) and 'پیکان' in brand:
        return 'سواری'
    if 'وانت' in model and 'پیکان' in brand:
        return 'وانت'
    if 'پرادو' in model:
        return 'پرادو'
    if 'لندکروز' in model:
        return 'لندکروز'
    if 'هایلوکس' in model:
        return 'هایلوکس'
    if 'یاریس' in model:
        return 'یاریس'
    if 'صندوق دار' in model and 'تیبا' in brand:
        return 'صندوق دار'
    if 'هاچ بک' in model and 'تیبا' in brand:
        return 'هاچ بک'
    if 'جی' in model and '4' in model and 'جک' in brand:
        return 'J4'
    if 'جی' in model and '5' in model and 'جک' in brand:
        return 'J5'
    if 'اس' in model and '3' in model and 'جک' in brand:
        return 'S3'
    if 'اس' in model and '5' in model and 'جک' in brand:
        return 'S5'
    if 'X7' in model and 'جیلی' in brand:
        return 'امگرند ایکس 7'
    if 'RV' in model and '7' in model and 'جیلی' in brand:
        return 'امگرند آر وی 7'
    if '7' in model and 'جیلی' in brand:
        return 'امگرند 7'
    if 'پلاس' in model and 'دنا' in brand:
        return 'پلاس'
    if 'دنا' in model and 'دنا' in brand:
        return 'معمولی'
    if '6' in model and 'دی اس' in brand:
        return 'DS6'
    if 'LX' in model and 'رانا' in brand:
        return 'LX'
    if 'EL' in model and 'رانا' in brand:
        return 'EL'
    if 'تلیسمان' in model or 'تالیسمان' in model:
        return 'تالیسمان'
    if '90' in model and 'رنو' in brand:
        return 'تندر 90'
    if 'مگان' in model and 'رنو' in brand:
        return 'مگان'
    if 'ریو' in model and 'کیا' in brand:
        return 'ریو'
    if 'سراتو' in model and 'کیا' in brand:
        return 'سراتو'
    if 'ES' in model and 'لکسوس' in brand:
        return 'سری ES'
    if 'GS' in model and 'لکسوس' in brand:
        return 'سری GS'
    if 'IS' in model and 'لکسوس' in brand:
        return 'سری IS'
    if 'LS' in model and 'لکسوس' in brand:
        return 'سری LS'
    if 'NX' in model and 'لکسوس' in brand:
        return 'سری NX'
    if 'RX' in model and 'لکسوس' in brand:
        return 'سری RX'
    if 'لیفان' in brand:
        return model.replace('لیفان', '').strip()
    if 'پاترول' in model and 'نیسان' in brand:
        return 'پاترول'
    if ('تی ینا' in model or 'تیانا' in model) and 'نیسان' in brand:
        return 'تی ینا'
    if 'هایما' in brand:
        return model.replace('هایما', '').strip()
    if ('ولستر' in model or 'ولوستر' in model) and 'هیوندای' in brand:
        return 'تی ینا'
    if 'سانتافه' in model and 'هیوندای' in brand:
        return 'سانتافه'
    if 'XC' in model and '90' in model and 'ولوو' in brand:
        return 'XC 90'
    if 'XC' in model and '60' in model and 'ولوو' in brand:
        return 'XC 60'

    return model


def normalize_brand(brand):
    brand = remove_extra_character_and_normalize(brand)
    brand = brand.upper()

    if 'آیودی' in brand or 'ایودی' in brand or 'آئودی' in brand or 'ائودی' in brand or 'AUDI' in brand:
        return 'آئودی'
    if 'آریسان' in brand or 'اریسان' in brand:
        return 'وانت'
    if 'آریو' in brand or 'اریو' in brand or 'زوتی' in brand:
        return 'زوتی آریو'
    if 'آلفارومئو' in brand or 'آلفارومیو' in brand or 'الفارومئو' in brand or 'الفارومیو' in brand or 'ALFA ROMEO' in brand:
        return 'آلفارومئو'
    if 'اس دبلیو ام' in brand or 'SWM' in brand:
        return 'اس دبلیو ام'
    if 'اس وای ام' in brand or 'SYM' in brand:
        return 'اس وای ام'
    if 'MG' in brand or 'ام جی' in brand:
        return 'ام جی'
    if 'BMW' in brand or 'ب ام و' in brand or 'بی ام و' in brand:
        return 'بی ام و'
    if 'DS' in brand or 'دی اس' in brand:
        return 'دی اس'
    if 'دیگر' in brand:
        return 'not_defined'
    if 'سیتروین' in brand or 'سیتروئن' in brand:
        return 'سیتروئن'
    if 'فولکس' in brand:
        return 'فولکس'
    if 'قطعات' in brand:
        return 'not_defined'

    return brand


def normalize_color(color):
    color = remove_extra_character_and_normalize(color)
    color = color.replace('ئ', 'ی')
    if 'سایر' in color:
        return 'not_defined'
    return color


def normalize_cash_installment(cash_installment):
    cash_installment = remove_extra_character_and_normalize(cash_installment)
    if 'اقساطی' in cash_installment or 'قسطی' in cash_installment:
        return 'قسطی'
    return cash_installment


def normalize_chassis_type(chassis_type):
    chassis_type = remove_extra_character_and_normalize(chassis_type)

    chassis_type = chassis_type.replace('هاچبک', 'هاچ بک')
    chassis_type = chassis_type.replace('هاچبك', 'هاچ بک')
    chassis_type = chassis_type.replace('هاچ بك', 'هاچ بک')

    if 'دیگر' in chassis_type:
        return 'not_defined'
    if 'سواری' in chassis_type or 'سدان' in chassis_type:
        return 'سواری'
    if 'کوپه' in chassis_type or 'کروک' in chassis_type:
        return 'کوپه/کروک'

    return chassis_type


def normalize_fuel(fuel):
    fuel = remove_extra_character_and_normalize(fuel)

    if 'دیزل' in fuel or 'گازوییل' in fuel or 'گازوئیل' in fuel or 'گازویل' in fuel:
        return 'گازوئیل'
    if 'هیبرید' in fuel:
        return 'هیبریدی'

    return fuel


def normalize_text(string: str):
    n = Normalizer()
    try:
        return n.normalize(string).replace('‌', ' ')
    except:
        return None


def remove_extra_character_and_normalize(text, listing=False):
    text = normalize_text(text)
    text = convert_digits(text)
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace("-", "")
    text = text.replace("_", "")
    text = text.replace(",", "")
    text = text.replace("،", "")
    text = text.replace("*", "")
    text = text.replace("/", "")
    text = text.replace(".", "")
    text = text.replace("#", "")
    text = text.replace("%", "")
    text = text.replace("$", "")
    text = text.replace("=", "")
    text = text.replace("+", "")
    text = text.replace("\\", "")
    text = text.replace("<", "")
    text = text.replace(">", "")
    text = text.replace("|", "")
    text = text.replace("[", "")
    text = text.replace("]", "")
    text = text.replace("{", "")
    text = text.replace("}", "")
    if listing:
        return [t.strip() for t in text.split()]
    return " ".join([t.strip() for t in text.split()])


def convert_digits(text):
    result = ""
    for c in text:
        if c == '۰':
            result += '0'
        elif c == '۱':
            result += '1'
        elif c == '۲':
            result += '2'
        elif c == '۳':
            result += '3'
        elif c == '۴':
            result += '4'
        elif c == '۵':
            result += '5'
        elif c == '۶':
            result += '6'
        elif c == '۷':
            result += '7'
        elif c == '۸':
            result += '8'
        elif c == '۹':
            result += '9'
        else:
            result += c
    return result


def normalize_and_compare(c1, c2):
    c1 = normalize_text(c1)
    c2 = normalize_text(c2)
    return c1 == c2
