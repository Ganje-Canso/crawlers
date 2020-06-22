# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest


class IranpelakSpider(scrapy.Spider):
    name = 'iranpelak'
    allowed_domains = ['iranpelak.com']
    start_urls = ['https://iranpelak.com/car-search']
    url = 'https://iranpelak.com/faces/root/car-search.xhtml'
    token = ""
    _pages = 3

    def parse(self, response):
        self.token = response.css('input[name="javax.faces.ViewState"]::attr(value)').get()
        self.logger.info(f"token: {self.token}")
        self.logger.info(f"form data: {self.create_form_data(1)}")

        yield FormRequest(url=self.url, method="POST", formdata=self.create_form_data(1), callback=self.parse_ads,
                          headers=self.headers)

    def parse_ads(self, response, page=2):
        # [href[:href.find('jsessionid') - 1] for href in (response.css('a::attr(href)').getall()) if 'ad-' in href]
        href_list = [f"https://iranpelak.com/{href}" for href in (response.css('a::attr(href)').getall()) if
                     'ad-' in href]
        self.logger.info(f"href_list length: {len(href_list)}")

        yield response.follow_all(href_list, callback=self.parse_ad, headers=self.headers)

        if page <= self._pages:
            yield FormRequest(url=self.url, method="POST", formdata=self.create_form_data(page),
                              callback=self.parse_ads,
                              headers=self.headers, cb_kwargs={"page": page + 1})

    def parse_ad(self, response):
        pass

    def create_form_data(self, page):
        return {
            "form": "form",
            "j_idt260": "NEWEST",
            "search-by-brand-input-textValue": "",
            "search-by-brand-input-textInput": "",
            "search-by-province-input-textValue": "",
            "search-by-province-input-textInput": "",
            "release-year-from-select-menu": "LESY_THAN_1979_1358",
            "release-year-to-select-menu": "Y_2020_1399",
            "odometer-from-select-menu-has-options": "KM_0",
            "odometer-to-select-menu-has-options": "KM_100000_PLUS",
            "name_input_text": "",
            "mobile_number_input_text": "",
            "password_input_text": "",
            "confirm_password_input_text": "",
            "mobile_number_sign_in_input_text": "",
            "password_sign_in_input_text": "",
            "modal - mobile_number_input_text": "",
            "javax.faces.ViewState": f"{self.token}",
            "javax.faces.source": "j_idt523",
            "javax.faces.partial.event": "rich:datascroller:onscroll",
            "javax.faces.partial.execute": "j_idt523 @ component",
            "javax.faces.partial.render": "@component",
            "j_idt523:page": f"{page}",
            "org.richfaces.ajax.component": "j_idt523",
            "j_idt523": "j_idt523",
            "rfExt": "null",
            "AJAX:EVENTS_COUNT": "1",
            "javax.faces.partial.ajax": "true"
        }

    headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Cookie": "_ga=GA1.2.658744249.1592760499; _gid=GA1.2.1211012335.1592760499; __auc=140e9b0a172d7ec7a4218567fa4; JSESSIONID=ad9c4dc16f95a58404c651b00eb8; __asc=006b9f3d172dad9da2f38ef21a8; _gat=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    }
