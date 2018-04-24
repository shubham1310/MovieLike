#For the crawling part #

Requirements:
scrapy

To run the crawler to get the movie names:
```bash
sh ScrapyIMDB/scrapyIMDB/script/crawl_movie_list.sh 2017, 2016, 2015,2014,2013,2012,2011,2010,2009,2008,2007
```

This will score the movie names and small details in a file in  ScrapyIMDB/scrapyIMDB/data/ called movie_list.csv

To then get the movie reviews, we have to the run the ./crawler.ipynb file. This essentially gets all the reviews and some additional movie details as well like movie plot on main page, poster image etc.
or can run

```bash
python crawler.py
```

The first part was taken from: https://github.com/vitid/ScrapyIMDB to get the movie names and was modified to get more movies as compared to the orignal numbers. The second part was written using Beautifulsoup and was written from scratch which does most of the work apart from high level movie information.


#For the search engine part #