# -*- coding: utf-8 -*-
import scrapy
import csv

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

        self.write_to_csv() # save all of the movies information to a csv

    def parse_movie(self, response):
        temp_dict = {} # make an empty dictionary to store a particular movie's information

        rating_info = response.css('div.ratingValue strong::attr(title)').extract()[0].split(' ')
        temp_dict['total_number_of_ratings'] = int(rating_info[3].replace(',', '')) # get total number of ratings
        temp_dict['rating_score'] = float(rating_info[0]) # get rating score

        temp_dict['genre'] = response.css('div.subtext a::text').extract()[0]

        isBudget = False
        isGross = False
        budget_info = response.xpath(
            '//div[contains(@class, "txt-block") and contains(.//h4, "Budget:")]/text()').extract()
        gross_info = response.xpath(
            '//div[contains(@class, "txt-block") and contains(.//h4, "Gross USA:")]/text()').extract()

        if (budget_info):
            budget_info = budget_info[1]
            budget_info = budget_info.strip()
            budget_info = budget_info.replace('$', '')
            temp_dict['budget'] = budget_info.replace(',', '')
        else:
            temp_dict['budget'] = None

        if (gross_info):
            gross_info = gross_info[1]
            gross_info = gross_info.strip()
            gross_info = gross_info.replace('$', '')
            temp_dict['gross_usa'] = gross_info.replace(',', '')
        else:
            temp_dict['gross_usa'] = None

        print(temp_dict)

    def write_to_csv(self):
        # with open('../../../movies_file.csv', mode='w') as movies_file:
        #     field_names = ['total_number_of_ratings', 'rating_score', 'genre', 'budget', 'gross_usa']
        #     writer = csv.DictWriter(movies_file, fieldnames=field_names)

        #     writer.writeheader()
            
        #     for movie in self.movies:
        #         writer.writerow(movie)

        return