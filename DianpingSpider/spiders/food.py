# -*- coding: utf-8 -*-

import scrapy

from DianpingSpider.items import Restaurant, Food, User


class DianpingSpider(scrapy.Spider):
    name = "food"
    #allowed_domains = ["www.dingping.com"]
#    start_urls = [
#        "http://www.dianping.com/shop/22813882"
#    ]

    def start_requests(self):
        yield scrapy.Request("http://www.dianping.com/ajax/json/shop/wizard/BasicHideInfoAjaxFP?shopId=22813882",
                headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"})


    def parse(self, response):
        

#        for sel in response.css("p.user-info"):
#    
#            user = User()
#
#            user['user_name'] = sel.css('a::text').extract()[0]
#            food['food_recommend_num'] = sel.css('em::text').re("[^()]+")[0]
#            
#            yield user

        print response.body()
