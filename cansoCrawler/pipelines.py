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
                f"call save_car_data({item['token']}, {item['source_id']}, {item['time']}, '{item['title']}', '{item['category']}', '{item['sub_category']}', '{item['province']}', '{item['city']}', '{item['neighbourhood']}', {item['production']}, {item['price']}, '{item['description']}', '{item['url']}', '{item['thumbnail']}', {item['latitude']}, {item['longitude']}, '{item['tell']}', {item['swap']}, '{item['brand']}', {item['consumption']}, '{item['color']}', '{item['cash_installment']}', '{item['gear_box']}', '{item['company']}', '{item['chassis_type']}', '{item['model']}', '{item['body_condition']}', '{item['fuel']}')")
            self.conn.commit()
        except:
            self.conn.rollback()
        return item
