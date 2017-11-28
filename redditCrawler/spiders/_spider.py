import scrapy
from datetime import datetime as dt
from redditCrawler.items import RedditItem
import pandas as pd
from scrapy import Spider, Request
import re
import odo

class RedditSpider(scrapy.Spider):
    name = "investing"
    end_date = '2017-11-26'
    start_urls = [
            'https://www.reddit.com/r/investing',
        ]
    '''
    def end_date(self):
        return end_date
    '''
    def parse(self, response):
        current_page = response.css('div.sitetable.linklisting div.thing ')
        next_page = response.css('span.next-button a::attr(href)').extract_first()
        for post in current_page:
            item = RedditItem()
            item['link'] = post.css('div::attr(data-url)').extract_first()
            item['subreddit'] = item['link'].split('/')[2]
            item['title'] = post.css('a.title.may-blank ::text').extract_first()
            item['date'] = post.css('time::attr(datetime)').extract_first()#.split('T')[0]
            item['upvotes'] = post.css('div.score.unvoted ::text').extract_first()
            #querying votes for threads not yet voted return '•'
            item['upvotes'] = 0 if item['upvotes'] == '•' else int(item['upvotes'])
            item['comment_count'] = post.css('div.entry.unvoted li.first a::text').extract_first().split()[0]
            item['comment_count'] = int(item['comment_count']) if item['comment_count'] != 'comment' else 0
            #if one == 1:
            request = Request(url = 'https://www.reddit.com'+ post.css('div::attr(data-url)').extract_first(), callback = self.parse_thread)
            request.meta['item'] = item
            #    one = None
            yield request

        if item['date'].split('T')[0] == self.end_date:
            yield
        else: yield Request(url = next_page, callback=self.parse)

            
    def parse_thread(self, response):
        item = response.meta['item']
        item['post'] = '\n'.join(response.css('div.sitetable.linklisting div.md p::text').extract())
        item['post_links'] = response.css('div.sitetable.linklisting div.md a::attr(href)').extract()
        #item['points'] = int(response.css('div.score span.number::text').extract_first())
        item['percent_upvoted'] = int(re.findall(r'\d+', response.css('div.score::text').extract()[1])[0])
        
        df = pd.DataFrame()#columns = ['author','time_stamp','score', 'comment', 'links'])
        for reply in response.css('div.commentarea div.thing'):
            new_df = pd.DataFrame()#(columns = ['author','time_stamp','score', 'comment', 'links'])
            try:
                #fetch author
                df.loc['new', 'comment_author'] = reply.css('a.author.may-blank::text').extract_first()
                #fetch scores
                df.loc['new', 'comment_score'] = int(reply.css('span.score.unvoted ::text').extract_first().split()[0]) #df.loc[author, 'score']
                #fetch comment
                df.loc['new', 'comment_reply'] = ''.join(reply.css('div.md')[0].css('::text').extract()[:-1])
                #fetch link shared
                comment_links = reply.css('div.md')[0].css('a::attr(href)').extract()
                df.loc['new', 'comment_links'] = reply.css('div.md')[0].css('a::attr(href)').extract() if len(comment_links) != 0 else None
                df.loc['new', 'comment_time_stamp'] = reply.css('time::attr(datetime)').extract_first()
                df = pd.concat([df,new_df], ignore_index = True)      
            except:
                pass
        df
        item['comments'] = df.to_dict('records') #'records' is passed as an argument to get a list of dictionary
        yield item

        #get top comments
        #get top comments points
        #get user

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


