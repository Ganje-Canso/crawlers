import datetime


def hash_token(token, source_id):
    import hashlib
    token = f"{token}{source_id}"
    return int(str(int(hashlib.sha1(str(token).encode()).hexdigest(), 16))[:18])


def get_time_stamp():
    return int(datetime.datetime.now().timestamp())


def get_persian_year():
    return int(datetime.datetime.today().year - 621)


def get_production(age):
    if age is None or age == -1 or age == '-1':
        return -1
    else:
        return get_persian_year() - int(age)
