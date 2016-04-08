# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Restaurant(Item):
    restaurantId = Field()         #21180353
    restaurantName = Field()       #周牛肉生态养生汤馆
    restaurantRegion = Field()     #双楠
    restaurantCategory = Field()   #火锅
    foods = Field()
    preferences = Field()


class Food(Item):
    foodName = Field()
    foodRecommendNum = Field()


class User(Item):
    userId = Field()
    userName = Field()


class Preference(Item):
    userId = Field()
    userName = Field()
    scores = Field()
    comment = Field()
    recommendFoods = Field()
