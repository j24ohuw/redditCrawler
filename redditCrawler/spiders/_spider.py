import scrapy
from redditCrawler.items import RedditItem

class RedditSpider(scrapy.Spider):
    name = "rInvesting"
    start_urls = [
            'https://www.reddit.com/r/investing',
        ]


    def parse(self, response):
        for post in response.css('div.sitetable.linklisting div.thing '):
            item = RedditItem()
            item['subreddit'] = post.css('div::attr(data-url)').extract()
            item['link'] = post.css('div::attr(data-url)').extract()
            item['title'] = post.css('a.title.may-blank ::text').extract()
            item['date'] = post.css('time::attr(datetime)').extract()
            item['upvoted'] = post.css('div.score.unvoted ::text').extract()

            yield item

            
##            yield {
##                
##                'title': post.css('a.title.may-blank ::text').extract(),
##                'link': post.css('div::attr(data-url)').extract(),
##                'upvoted': post.css('div.score.unvoted ::text').extract(),
##                'date': post.css('time::attr(datetime)').extract(),
##                'comment': post.css('li.first a ::text').extract(),  
##
##                }
        
##        titles = response.css("a.title.may-blank ::text").extract()
##        links = response.css('p.title a::attr(href)').extract()
##        block = response.css('div.sitetable.linklisting div.thing ')
##        links = block.css('div::attr(data-url)').extract

##        page = response.url.split("/")[-2]
##        filename = 'rInvesting-%s.html' % page
##        with open(filename, 'wb') as f:
##            f.write(response.body)
##        self.log('Saved file %s' % filename)




#nextP = response.xpath('//span[@class="next-button"]/a/@href').extract()
#if link, copy the link address
#if post, copy the the post context
#bitcoin/cryptocurrency
#questioin - ?
#education
#doom and gloom
#tech
#graham/value/buffet/berkshire
#how do I group repeated words/themes/contexts for a given subreddit?
#reconstruct a webpage with garbage filtering

##titles = response.xpath('//p[@class="title"]/a[@class="title may-blank "]/text()').extract()
##response.css('li.next a::attr(href)').extract_first()
## b = response.css('p.title a::attr(href)').extract()
