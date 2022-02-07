# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0413573/']

    def parse(self, response):
        '''
        A parsing method that navigates from a title's home page to its Cast and Crew page.
        '''
        # string to append to initial url
        next_page = "fullcredits/"

        # append string and call next parsing method
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        '''
        A parsing method that navigates to each actor's profile in a title's IMDB
        Cast and Crew page
        '''
    
        # a list of all links to each actor's IMDB page
        next_page_list = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        # navigate to each actor's IMDB page
        for next_page in next_page_list:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        '''
        A parsing method for retrieving all movies and TV shows that an actor
        is listed as performing in on IMDB.
        '''
        
        # get actor name
        actor_name = response.css("span.itemprop::text").get()
        
        # get all movie and TV show titles
        for element in response.css("div.filmo-row"):
            element = response.css("b")
            movie_or_tv_name = element.css("a::text").getall()

            this_title = "Grey's Anatomy"
            movie_or_tv_name = ['!!!' + a for a in movie_or_tv_name if this_title not in a]

        # yield dictionary of data
        yield {
            "actor" : actor_name,
            "movie_or_tv_name": movie_or_tv_name,
        }


