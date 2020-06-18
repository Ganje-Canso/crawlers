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
    if 'موزاییک' in floor_covering or 'موزائیک' in floor_covering or 'موزاییك' in floor_covering or 'موزائیك':
        return 'موزائیک'
    if 'موکت' in floor_covering:
        return 'موکت'
    return 'not_defined'


def normalize_car_item(item):
    pass


def convert_alphabetic_number_to_integer(number):
    if number == 'بدون اتاق':
        return 0
    elif number == 'یک':
        return 1
    elif number == 'دو':
        return 2
    elif number == 'سه':
        return 3
    elif number == 'چهار':
        return 4
    else:
        return 5


def normalize_text(string: str):
    n = Normalizer()
    try:
        return n.normalize(string).replace('‌', ' ')
    except:
        return None


def search(key, title):
    if key in title:
        return True
    else:
        return False


def normalize_category(source, category, title):
    new_category = ""
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    query = "SELECT keys,CANSO FROM tb_" + source + " WHERE sheypoor='" + category.replace('-', ' ') + "';"
    print(query)
    keys, new_category = cur.execute(
        "SELECT keys,CANSO FROM tb_sheypoor WHERE sheypoor='" + category.replace('-', ' ') + "';").fetchall()[0]
    new_category = new_category.split(',')
    if keys is not None:
        keys = keys.split(',')

        if len(keys) != 0:
            for i in range(0, len(keys)):
                if search(keys[i], title):
                    new_category = new_category[i]
                else:
                    new_category = new_category[0]  # Default
    else:
        new_category = new_category[0]
    cur.close()
    db.close()
    return new_category


def remove_extra_character_and_normalize(text, listing=False):
    text = normalize_text(text)
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


def normalize_and_compare(c1, c2):
    c1 = normalize_text(c1)
    c2 = normalize_text(c2)
    return c1 == c2
