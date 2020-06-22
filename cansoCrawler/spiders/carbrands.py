# -*- coding: utf-8 -*-
import scrapy
import json


class CarbrandsSpider(scrapy.Spider):
    name = 'carbrands'
    allowed_domains = ['bama.ir']
    start_urls = ['https://bama.ir/api/search/brands/']

    def parse(self, response):
        brand_list = json.loads(response.body.decode('UTF-8'))

        for brand in brand_list:
            yield response.follow(url=f"https://bama.ir/api/search/models/{brand['Value'].split(',')[0]}",
                                  callback=self.parse_model, cb_kwargs={"brand": brand})

    def parse_model(self, response, brand):
        model_list = json.loads(response.body.decode('UTF-8'))
        model_name_list = []
        for model in model_list:
            model_name_list.append(model["Text"])
        if len(model_name_list) == 0:
            self.logger.info(f"model empty for: {brand['Text']}")
        yield {
            "brand": brand["Text"],
            "models": model_name_list
        }
