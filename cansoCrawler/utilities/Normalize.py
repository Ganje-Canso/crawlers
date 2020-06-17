import sqlite3

from hazm import Normalizer


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
