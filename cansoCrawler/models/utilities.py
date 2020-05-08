from scrapy.utils.log import logger
import psycopg2 as psycopg2

conn = psycopg2.connect(database="cansotest", user="canso", password="oJ72k2cLdgfWN7ruujHJb8A1jOXKxSjK", host="canso.ir",
                             port="5432")
cursor = conn.cursor()


def get_province(city: str):
    try:
        cursor.execute(
            "select name from api_province where id=(select province_id from api_city where name=%s);",
            (city,)
        )
        data = cursor.fetchall()
        return data[0][0]
    except Exception as e:
        logger.critical(e)
        return 'not_defined'


def get_item(table_name: str, token: str):
    try:
        cursor.execute(
            "select source_id from {} where token=%s;".format(table_name),
            (token, )
        )
        data = cursor.fetchall()
        return data[0][0]
    except Exception as e:
        logger.critical(e)
        return 'not_defined'
