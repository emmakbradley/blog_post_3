# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0413573/']

    def parse(self, response):
        
        next_page = "fullcredits/"

        if next_page:
            next_page = response.urljoin(next_page)
            # callback should be the next parse method
            yield scrapy.Request(next_page, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        
        next_page_list = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        for next_page in next_page_list:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse_actor_page)

    def parse_actor_page(self, response):

        actor_name = response.css("span.itemprop::text").get()
        
        for element in response.css("div.filmo-row"):
            element = response.css("b")
            movie_or_tv_name = element.css("a::text").getall()

            this_title = "Grey's Anatomy"
            movie_or_tv_name = [a for a in movie_or_tv_name if this_title not in a]

        yield {
            "actor" : actor_name,
            "movie_or_tv_name": movie_or_tv_name,
        }


