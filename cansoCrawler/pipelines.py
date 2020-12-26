# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.utils.log import logger
import psycopg2 as psycopg2

from cansoCrawler.utilities.Normalize import normalize_item
from cansoCrawler.utilities.configs import server_db, local_db


class CansocrawlerPipeline(object):

    def open_spider(self, spider):
        # db_config = local_db
        db_config = server_db
        self.conn = psycopg2.connect(
            database=db_config["database"],
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"])
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        item_base_name = item.__class__.__base__.__name__.lower()

        ad_type = 'home' if 'home' in item_base_name else 'car'

        normalize_item(item, ad_type)

        if ad_type == 'home':
            if self.not_exist(item['token'], ad_type):
                self.save_home_data(item)
        elif ad_type == 'car':
            if self.not_exist(item['token'], ad_type):
                self.save_car_data(item)

    def save_home_data(self, item):
        try:
            self.cursor.execute(
                "insert into home (" +
                (("token," if self.insertThis(item["token"]) else "") +
                 ("source_id," if self.insertThis(item["source_id"]) else "") +
                 ("time," if self.insertThis(item["time"]) else "") +
                 ("title," if self.insertThis(item["title"]) else "") +
                 ("category," if self.insertThis(item["category"]) else "") +
                 ("sub_category," if self.insertThis(item["sub_category"]) else "") +
                 ("province," if self.insertThis(item["province"]) else "") +
                 ("city," if self.insertThis(item["city"]) else "") +
                 ("neighbourhood," if self.insertThis(item["neighbourhood"]) else "") +
                 ("advertiser," if self.insertThis(item["advertiser"]) else "") +
                 ("production," if self.insertThis(item["production"]) else "") +
                 ("room," if self.insertThis(item["room"]) else "") +
                 ("area," if self.insertThis(item["area"]) else "") +
                 ("price," if self.insertThis(item["price"]) else "") +
                 ("deposit," if self.insertThis(item["deposit"]) else "") +
                 ("rent," if self.insertThis(item["rent"]) else "") +
                 ("description," if self.insertThis(item["description"]) else "") +
                 ("url," if self.insertThis(item["url"]) else "") +
                 ("thumbnail," if self.insertThis(item["thumbnail"]) else "") +
                 ("latitude," if self.insertThis(item["latitude"]) else "") +
                 ("longitude," if self.insertThis(item["longitude"]) else "") +
                 ("tell," if self.insertThis(item["tell"]) else "") +
                 ("swap," if self.insertThis(item["swap"]) else "") +
                 ("administrative_document," if self.insertThis(item["administrative_document"]) else "") +
                 ("parking," if self.insertThis(item["parking"]) else "") +
                 ("elevator," if self.insertThis(item["elevator"]) else "") +
                 ("storeroom," if self.insertThis(item["storeroom"]) else "") +
                 ("swap_deposit_rent," if self.insertThis(item["swap_deposit_rent"]) else "") +
                 ("balcony," if self.insertThis(item["balcony"]) else "") +
                 ("estate_floor," if self.insertThis(item["estate_floor"]) else "") +
                 ("estate_direction," if self.insertThis(item["estate_direction"]) else "") +
                 ("package," if self.insertThis(item["package"]) else "") +
                 ("kitchen," if self.insertThis(item["kitchen"]) else "") +
                 ("cooler," if self.insertThis(item["cooler"]) else "")).strip(',') +
                (",floor_covering" if self.insertThis(item["floor_covering"]) else "") +
                ") " +
                "values (" +
                ((f"{item['token']}," if self.insertThis(item["token"]) else "") +
                 (f"{item['source_id']}," if self.insertThis(item["source_id"]) else "") +
                 (f"{item['time']}," if self.insertThis(item["time"]) else "") +
                 (f"'{item['title']}'," if self.insertThis(item["title"]) else "") +
                 (f"'{item['category']}'," if self.insertThis(item["category"]) else "") +
                 (f"'{item['sub_category']}'," if self.insertThis(item["sub_category"]) else "") +
                 (f"'{item['province']}'," if self.insertThis(item["province"]) else "") +
                 (f"'{item['city']}'," if self.insertThis(item["city"]) else "") +
                 (f"'{item['neighbourhood']}'," if self.insertThis(item["neighbourhood"]) else "") +
                 (f"'{item['advertiser']}'," if self.insertThis(item["advertiser"]) else "") +
                 (f"{item['production']}," if self.insertThis(item["production"]) else "") +
                 (f"{item['room']}," if self.insertThis(item["room"]) else "") +
                 (f"{item['area']}," if self.insertThis(item["area"]) else "") +
                 (f"{item['price']} ," if self.insertThis(item["price"]) else "") +
                 (f"{item['deposit']}," if self.insertThis(item["deposit"]) else "") +
                 (f"{item['rent']}," if self.insertThis(item["rent"]) else "") +
                 (f"'{item['description']}'," if self.insertThis(item["description"]) else "") +
                 (f"'{item['url']}'," if self.insertThis(item["url"]) else "") +
                 (f"'{item['thumbnail']}'," if self.insertThis(item["thumbnail"]) else "") +
                 (f"{item['latitude']}," if self.insertThis(item["latitude"]) else "") +
                 (f"{item['longitude']}," if self.insertThis(item["longitude"]) else "") +
                 (f"'{item['tell']}'," if self.insertThis(item["tell"]) else "") +
                 (f"{item['swap']}," if self.insertThis(item["swap"]) else "") +
                 (f"{item['administrative_document']}," if self.insertThis(item["administrative_document"]) else "") +
                 (f"{item['parking']}," if self.insertThis(item["parking"]) else "") +
                 (f"{item['elevator']}," if self.insertThis(item["elevator"]) else "") +
                 (f"{item['storeroom']}," if self.insertThis(item["storeroom"]) else "") +
                 (f"{item['swap_deposit_rent']}," if self.insertThis(item["swap_deposit_rent"]) else "") +
                 (f"{item['balcony']}," if self.insertThis(item["balcony"]) else "") +
                 (f"{item['estate_floor']}," if self.insertThis(item["estate_floor"]) else "") +
                 (f"'{item['estate_direction']}'," if self.insertThis(item["estate_direction"]) else "") +
                 (f"{item['package']}," if self.insertThis(item["package"]) else "") +
                 (f"'{item['kitchen']}'," if self.insertThis(item["kitchen"]) else "") +
                 (f"{item['cooler']}," if self.insertThis(item["cooler"]) else "")).strip(',') +
                (f",'{item['floor_covering']}'" if self.insertThis(item["floor_covering"]) else "") +
                " )")
            self.conn.commit()
        except:
            self.conn.rollback()
            logger.critical(f"pipeline => not_exist: {e}")
        return item

    def save_car_data(self, item):
        try:
            self.cursor.execute(
                "insert into car (" +
                (("token," if self.insertThis(item["token"]) else "") +
                 ("source_id," if self.insertThis(item["source_id"]) else "") +
                 ("time," if self.insertThis(item["time"]) else "") +
                 ("title," if self.insertThis(item["title"]) else "") +
                 ("category," if self.insertThis(item["category"]) else "") +
                 ("sub_category," if self.insertThis(item["sub_category"]) else "") +
                 ("province," if self.insertThis(item["province"]) else "") +
                 ("city," if self.insertThis(item["city"]) else "") +
                 ("neighbourhood," if self.insertThis(item["neighbourhood"]) else "") +
                 ("production," if self.insertThis(item["production"]) else "") +
                 ("price," if self.insertThis(item["price"]) else "") +
                 ("description," if self.insertThis(item["description"]) else "") +
                 ("url," if self.insertThis(item["url"]) else "") +
                 ("thumbnail," if self.insertThis(item["thumbnail"]) else "") +
                 ("latitude," if self.insertThis(item["latitude"]) else "") +
                 ("longitude," if self.insertThis(item["longitude"]) else "") +
                 ("tell," if self.insertThis(item["tell"]) else "") +
                 ("swap," if self.insertThis(item["swap"]) else "") +
                 ("brand," if self.insertThis(item["brand"]) else "") +
                 ("consumption," if self.insertThis(item["consumption"]) else "") +
                 ("color," if self.insertThis(item["color"]) else "") +
                 ("cash_installment," if self.insertThis(item["cash_installment"]) else "") +
                 ("gear_box," if self.insertThis(item["gear_box"]) else "") +
                 ("company," if self.insertThis(item["company"]) else "") +
                 ("chassis_type," if self.insertThis(item["chassis_type"]) else "") +
                 ("model," if self.insertThis(item["model"]) else "") +
                 ("body_condition," if self.insertThis(item["body_condition"]) else "")).strip(',') +
                (",fuel" if self.insertThis(item["fuel"]) else "") +
                ") " +
                "values (" +
                ((f"{item['token']}," if self.insertThis(item["token"]) else "") +
                 (f"{item['source_id']}," if self.insertThis(item["source_id"]) else "") +
                 (f"{item['time']}," if self.insertThis(item["time"]) else "") +
                 (f"'{item['title']}'," if self.insertThis(item["title"]) else "") +
                 (f"'{item['category']}'," if self.insertThis(item["category"]) else "") +
                 (f"'{item['sub_category']}'," if self.insertThis(item["sub_category"]) else "") +
                 (f"'{item['province']}'," if self.insertThis(item["province"]) else "") +
                 (f"'{item['city']}'," if self.insertThis(item["city"]) else "") +
                 (f"'{item['neighbourhood']}'," if self.insertThis(item["neighbourhood"]) else "") +
                 (f"{item['production']}," if self.insertThis(item["production"]) else "") +
                 (f"{item['price']}," if self.insertThis(item["price"]) else "") +
                 (f"'{item['description']}'," if self.insertThis(item["description"]) else "") +
                 (f"'{item['url']}'," if self.insertThis(item["url"]) else "") +
                 (f"'{item['thumbnail']}'," if self.insertThis(item["thumbnail"]) else "") +
                 (f"{item['latitude']}," if self.insertThis(item["latitude"]) else "") +
                 (f"{item['longitude']}," if self.insertThis(item["longitude"]) else "") +
                 (f"'{item['tell']}'," if self.insertThis(item["tell"]) else "") +
                 (f"{item['swap']}," if self.insertThis(item["swap"]) else "") +
                 (f"'{item['brand']}'," if self.insertThis(item["brand"]) else "") +
                 (f"{item['consumption']}," if self.insertThis(item["consumption"]) else "") +
                 (f"'{item['color']}'," if self.insertThis(item["color"]) else "") +
                 (f"'{item['cash_installment']}'," if self.insertThis(item["cash_installment"]) else "") +
                 (f"'{item['gear_box']}'," if self.insertThis(item["gear_box"]) else "") +
                 (f"'{item['company']}'," if self.insertThis(item["company"]) else "") +
                 (f"'{item['chassis_type']}'," if self.insertThis(item["chassis_type"]) else "") +
                 (f"'{item['model']}'," if self.insertThis(item["model"]) else "") +
                 (f"'{item['body_condition']}'," if self.insertThis(item["body_condition"]) else "")).strip(',') +
                (f",'{item['fuel']}'" if self.insertThis(item["fuel"]) else "") +
                " )")
            self.conn.commit()
        except:
            self.conn.rollback()
            logger.critical(f"pipeline => not_exist: {e}")
        return item

    def not_exist(self, token, ad_type):
        try:
            self.cursor.execute(f"select count(token) from {ad_type} where token = {token}")
            data = self.cursor.fetchall()
            if int(data[0][0]) > 0:
                return False
        except Exception as e:
            self.conn.rollback()
            logger.critical(f"pipeline => not_exist: {e}")
        return True

    def insertThis(self, v):
        return str(v) != '-1' and v != 'not_defined' and v != 'notdefined' and v != 'not defined' and str(v) != '-1.0' and v != 'not-defined' \
               and v != 'NOTDEFINED' and v != 'NOT DEFINED' and len(str(v)) != 0 and v is not None
