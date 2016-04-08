# -*- coding: utf-8 -*-

import scrapy

from DianpingSpider.items import Restaurant, Food, User


class DianpingSpider(scrapy.Spider):
    name = "one"
    #allowed_domains = ["www.dingping.com"]
    start_urls = [
        'http://www.dianping.com/search/category/8/10/g0r0'
    ]

    def start_requests(self):
        yield scrapy.Request("http://www.dianping.com/search/category/8/10/g0r0",
                headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"})

    def parse(self, response):

        for sel in response.css("div#shop-all-list > ul > li"):

            restaurant = Restaurant()
            restaurant['restaurant_id'] = sel.css('div.txt > div.tit > a::attr(href)').extract()[0].split('/')[-1]
            restaurant['restaurant_name'] = sel.css('div.txt > div.tit > a::attr(title)').extract()[0]
            restaurant['restaurant_category'] = sel.css('div.txt > div.tag-addr > a > span::text').extract()[0]
            restaurant['restaurant_region'] = sel.css('div.txt > div.tag-addr > a > span::text').extract()[1]
            
            url = "http://www.dianping.com/shop/" + restaurant['restaurant_id']
            
            yield scrapy.Request(url,
                    meta = {'restaurant': restaurant},
                    callback = self.parse_food,
                    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"})

#        next_page = response.css("div.page > a.next::attr(href)").extract()[0]
#
#        if next_page:
#            
#            url = response.urljoin(next_page)
#            yield scrapy.Request(url,
#                    callback = self.parse,
#                    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"})


    def parse_food(self, response):

        restaurant = response.meta['restaurant']

        foods = []

        for sel in response.css("p.recommend-name > a"):
            
            print "chenyixiao" 
            food = Food()
            food['food_name'] = sel.xpath('@title').extract()[0]
            food['food_recommend_num'] = sel.css('em::text').re("[^()]+")[0]
            foods.append(dict(food))
            

        restaurant['foods'] = foods

        yield restaurant




