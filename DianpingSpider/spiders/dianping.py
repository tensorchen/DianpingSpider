# -*- coding: utf-8 -*-

import scrapy
import urllib2
import json
import errno

from DianpingSpider.items import Restaurant, Food, User, Preference
from socket   import error as SocketError


class DianpingSpider(scrapy.Spider):
    name = "dianping"
    #allowed_domains = ["www.dingping.com"]
    start_urls = [
        'http://www.dianping.com/search/category/8/10/g0r0'
    ]



    def start_requests(self):
        main_page = "http://www.dianping.com/search/category/8/10/g0r0"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
        yield scrapy.Request(main_page,
                headers = {'User-Agent':user_agent})

    def parse(self, response):

        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"


        for sel in response.css("div#shop-all-list > ul > li"):

            restaurant = Restaurant()
            restaurant['restaurantId'] = long(sel.css('div.txt > div.tit > a::attr(href)').extract()[0].split('/')[-1])
            restaurant['restaurantName'] = sel.css('div.txt > div.tit > a::attr(title)').extract()[0]
            restaurant['restaurantCategory'] = sel.css('div.txt > div.tag-addr > a > span::text').extract()[0]
            restaurant['restaurantRegion'] = sel.css('div.txt > div.tag-addr > a > span::text').extract()[1]
             
            food_url = "http://www.dianping.com/ajax/json/shop/wizard/BasicHideInfoAjaxFP?shopId=" + str(restaurant['restaurantId'])

            request = urllib2.Request(food_url)
            request.add_header('User-Agent', user_agent)

            try:
                food_data = urllib2.urlopen(request).read()
            except (urllib2.HTTPError, urllib2.URLError, SocketError) as err:
                food_data = ""
           # except (urllib2.HTTPError, urllib2.URLError) as err:
           #     food_data = ""
           #     print "URLLIB2: ", err


            restaurant['foods'] = []

            try:
                food_json = json.loads(food_data)
                foods = food_json['msg']['shopInfo']['dishTags'][:-1].split('|')
            except (TypeError, ValueError) as err:
                foods = []
                print "Mark: ", err

            for f in foods: 
                
                food = Food()
                food['foodName'] = f.split(',')[0]
                
                try:
                    num = int(f.split(',')[1])
                except (UnicodeEncodeError, IndexError) as err:
                    num = 0
                    print "Mark:", err

                food['foodRecommendNum'] = num 

                restaurant['foods'].append(dict(food))
           
            yield scrapy.Request("http://www.dianping.com/shop/" + str(restaurant['restaurantId']),
                    meta = {'restaurant': restaurant},
                    callback = self.parse_user_comment,
                    headers = {'User-Agent': user_agent})

        next_page = response.css("div.page > a.next::attr(href)").extract()[0]

        if next_page:
            
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback = self.parse,
                    headers = {'User-Agent':user_agent}) 



    def parse_user_comment(self, response):
        
        restaurant = response.meta['restaurant']
        preferences = []

        for sel in response.css('li.comment-item'):
            
            preference = Preference()
            try:
                preference['userId'] = long(sel.css('p.user-info > a::attr(href)').extract()[0].split('/')[-1])
            except IndexError as err:
                preference['userId'] = 0

            preference['userName'] = sel.css('p.user-info > a::text').extract()[0]

            preference['scores'] = [] 
            for score in sel.css('div.content > p.shop-info > span.item::text'):
                #preference['scores'].append(int(score.extract()[0].split(":")[-1].strip()))
                preference['scores'].append(int(score.extract()[-1]))

#            preference['comment'] = sel.css('div.content > p.desc::text').extract()

            preference['recommendFoods'] = []
            for food in sel.css('div.content > dl > dd > a::text'):
                preference['recommendFoods'].append(food.extract())

            preferences.append(dict(preference))

        restaurant['preferences'] = preferences

        yield restaurant


