# -*- coding: utf-8 -*-
import scrapy
import re, csv, os

class ImdbSpiderSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/chart/top?ref_=nv_mv_250']

    movies = {} # dictionary to store all of the movies information
    i = 0 # iterator

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse) # send a request to the starting url
    
    def parse(self, response):
        links = response.css('td.titleColumn a::attr(href)').extract() # get all of the movies links

        for link in links:
            yield response.follow('https://www.imdb.com' + link, callback=self.parse_movie) # send a request to each movie url

    def parse_movie(self, response):
        temp_dict = {} # make an empty dictionary to store a particular movie's information

        rating_info = response.css('div.ratingValue strong::attr(title)').extract()[0].split(' ')
        temp_dict['total_number_of_ratings'] = int(rating_info[3].replace(',', '')) # get total number of ratings
        temp_dict['rating_score'] = float(rating_info[0]) # get rating score

        temp_dict['genre'] = ','.join(response.css('div.subtext a::text').extract()[:-1]) # get genre
        print(temp_dict['genre'])

        budget_info = response.xpath(
            '//div[contains(@class, "txt-block") and contains(.//h4, "Budget:")]/text()').extract() # get budget
        gross_info = response.xpath(
            '//div[contains(@class, "txt-block") and contains(.//h4, "Gross USA:")]/text()').extract() # get gross usa

        if (budget_info):
            budget_info = budget_info[1]
            temp_dict['budget'] = int(re.sub('\D', '', budget_info)) # remove characters except digits
        else:
            temp_dict['budget'] = None

        if (gross_info):
            gross_info = gross_info[1]
            temp_dict['gross_usa'] = int(re.sub('\D', '', gross_info)) # remove characters except digits
        else:
            temp_dict['gross_usa'] = None

        self.movies[str(self.i)] = temp_dict
        self.i += 1

    def closed(self, reason):
        if not os.path.exists('../data'):
            os.makedirs('../data')

        # save all of the movies information to a csv
        with open('../data/movies_file.csv', mode='w+', newline='') as movies_file:
            field_names = ['total_number_of_ratings', 'rating_score', 'genre', 'budget', 'gross_usa']
            writer = csv.DictWriter(movies_file, fieldnames=field_names)

            writer.writeheader() # write the header to the csv
            
            for key, movie in self.movies.items():
                writer.writerow(movie) # write movie information to the csv