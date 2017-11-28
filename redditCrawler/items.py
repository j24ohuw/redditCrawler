# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class RedditItem(scrapy.Item):
    subreddit = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    upvotes = scrapy.Field()
    comment_count = scrapy.Field()
    post = scrapy.Field()
    post_links = scrapy.Field()
    points = scrapy.Field()
    percent_upvoted = scrapy.Field()
    thread_df = scrapy.Field()
    #top_comment = Field()
##
##class RedditcrawlerItem(scrapy.Item):
##    # define the fields for your item here like:
##    # name = scrapy.Field()
##    pass
