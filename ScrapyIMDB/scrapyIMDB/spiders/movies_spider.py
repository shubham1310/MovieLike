import scrapy

class MoviesSpider(scrapy.Spider):
    '''
    Crawl 20 movies per year. Sorted by num_votes(to ensure that the movie has enough review contents)
    and try to cover movies with good and mixed reviews.
    '''
    name = "movie_list"
    #noted: one loaded page contains 50 movies
    urlTemplate = "http://www.imdb.com/search/title?year={year},{year}&title_type=feature&sort=num_votes,desc&page={page}&ref_=adv_nxt"

    def start_requests(self):
        self.crawlYears = getattr(self,'crawlYears',"2010").split(",")

        for year in self.crawlYears:
            for j in range(1,100):
                yield scrapy.Request(url=self.getUrl(year,pagenum = str(j) ), callback=self.parse)

    def getUrl(self,year,pagenum = 1):
        return self.urlTemplate.replace("{year}",year).replace("{page}",pagenum)

    def parse(self, response):
        #noted: 50 contents per page!!
        contents = response.xpath("//div[@class='lister-item mode-advanced']")

        #inrement by 2 for added coverage
        for index in range(0,40,2):
            content = contents[index]
            movieName = content.xpath("div[@class='lister-item-content']/h3/a/text()").extract_first()
            titleId = content.xpath("div[@class='lister-item-content']/h3/a/@href").extract_first().split("/")[2]
            genres = content.xpath("div[@class='lister-item-content']/p/span[@class='genre']/text()").extract_first().replace("\n","").replace(" ","")
            runtime = content.xpath("div[@class='lister-item-content']/p/span[@class='runtime']/text()").extract_first()
            reviewScore = content.xpath("div[@class='lister-item-content']/div[@class='ratings-bar']/div/strong/text()").extract_first()
            yield{
                "name":movieName,
                "titleId":titleId,
                "genres":genres,
                "runtime":runtime,
                "reviewScore":reviewScore
            }
