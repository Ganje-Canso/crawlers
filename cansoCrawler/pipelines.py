# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

import psycopg2 as psycopg2


class CansocrawlerPipeline(object):

    def open_spider(self, spider):
        self.conn = psycopg2.connect(database="canso", user="postgres", password="104603415204", host="localhost",
                                     port="5433")
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        item_base_name = item.__class__.__base__.__name__.lower()
        if 'home' in item_base_name:
            self.save_home_data(item)
        elif 'car' in item_base_name:
            self.save_car_data(item)

    def save_home_data(self, item):
        try:
            self.cursor.execute(
                f"call save_home_data({item['token']}, {item['source_id']}, {item['time']}, '{item['title']}' ,'{item['category']}' ,'{item['sub_category']}' ,'{item['province']}' ,'{item['city']}' , '{item['neighbourhood']}' ,'{item['advertiser']}' ,{item['production']} , {item['room']}, {item['area']}, {item['price']} , {item['deposit']}, {item['rent']}, '{item['description']}', '{item['url']}', '{item['thumbnail']}', {item['latitude']}, {item['longitude']}, '{item['tell']}', {item['swap']}, {item['administrative_document']}, {item['parking']}, {item['elevator']}, {item['storeroom']}, {item['swap_deposit_rent']}, {item['balcony']}, {item['estate_floor']}, '{item['estate_direction']}', {item['package']}, '{item['kitchen']}', {item['cooler']}, '{item['floor_covering']}')")
            self.conn.commit()
        except:
            self.conn.rollback()
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
                ")")
            self.conn.commit()
        except:
            self.conn.rollback()
        return item

    def insertThis(self, v):
        return str(v) != '-1' and v != 'not_defined'
