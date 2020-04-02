# -*- coding: utf-8 -*-
import scrapy


class BamaSpider(scrapy.Spider):
    name = 'bama'
    allowed_domains = ['bama.ir']
    base_url = ""

    def start_requests(self):
        url = "https://bama.ir/"
        category = getattr(self, "category", "car")
        url = url + category + "/"
        self.base_url = url + "all-brands/all-models/all-trims?page="
        yield scrapy.Request(self.base_url + "{}".format(1), callback=self.parse)

    def parse(self, response, page=2):
        self.logger.info("get ads from page: %s", page - 1)
        ad_links = response.css('div#adlist li').xpath('./a/@href').getall()
        yield from response.follow_all(ad_links, callback=self.parse_ad, cb_kwargs={"page": page - 1})

        # get next page
        if page <= 5:
            yield response.follow(self.base_url + "{}".format(page), callback=self.parse,
                                  cb_kwargs={"page": page + 1})

    def parse_ad(self, response, page):
        if "news" in response.request.url:
            return
        self.logger.info("get ad from: %s", response.request.url)
        info_right = response.css('div.inforight')
        description = response.css('div.addetaildesc').xpath('./span/text()').get(default="not_defined").strip()

        yield {
            "subject": self.create_subject(info_right.xpath('./div[1]/div[1]/h1[1]/span/text()').getall()),
            "url": response.request.url,
            "brand": response.css('div.breadcrumb-div-section ol').xpath('./li[3]/a/span/text()').get().strip(),
            "model": response.css('div.breadcrumb-div-section ol').xpath('./li[4]/a/span/text()').get().strip(),
            "page": page,
            "description": description,
            "details": self.create_details(info_right.xpath('./p'))
        }

    def create_details(self, _details):
        details = {"empty": False}
        for detail in _details:
            _class = detail.css('::attr(class)').get()
            if _class == "phone-mobile-block":
                continue
            key = detail.xpath('./span[1]/text()').get().strip()
            if key == "رنگ":
                value = detail.xpath('./span[2]/f[1]/text()').get().strip()
                details["رنگ داخل"] = detail.xpath('./span[2]/f[4]/text()').get().strip()
            else:
                value = detail.xpath('./span[2]/text()').get().strip()
            details[key] = value
        return {"empty": True} if len(details) == 1 else details

    def create_subject(self, sections):
        subject = ""
        for subject_section in sections:
            subject += subject_section.strip()
        return subject
