import scrapy

class RedditSpider(scrapy.Spider):
    name = "rInvesting"
    start_urls = [
            'https://www.reddit.com/r/investing',
        ]


    def parse(self, response):
        for post in response.css('div.sitetable.linklisting div.thing '):
            yield {
                'titles': post.css("a.title.may-blank ::text").extract(),
                'links': post.css('div::attr(data-url)').extract(),
                }
##        titles = response.css("a.title.may-blank ::text").extract()
##        links = response.css('p.title a::attr(href)').extract()
##        block = response.css('div.sitetable.linklisting div.thing ')
##        links = block.css('div::attr(data-url)').extract

##        page = response.url.split("/")[-2]
##        filename = 'rInvesting-%s.html' % page
##        with open(filename, 'wb') as f:
##            f.write(response.body)
##        self.log('Saved file %s' % filename)


