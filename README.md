# For the crawling part 

Requirements:<br>
scrapy<br>
nltk<br>

To run the crawler to get the movie names:
```bash
cd ScrapyIMDB/script
sh ./crawl_movie_list.sh 2017, 2016, 2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000
```

This will score the movie names and small details in a file in  ScrapyIMDB/data/ called movie_list.csv

To then get the movie reviews: 

we have to the run the ./crawler.ipynb file. This essentially gets all the reviews (cleans the data by stemming etc) and some additional movie details as well like movie plot on main page, poster image etc.


Or we can run this file directly

```bash
python crawler.py
```

The first part was taken from: https://github.com/vitid/ScrapyIMDB to get the movie names and was modified to get more movies as compared to the orignal numbers. The second part was written using Beautifulsoup and was written from scratch which does most of the work apart from high level movie information.


# For the search engine part

Follow the steps in the readme at https://github.com/shubham1310/imdbcrawler/tree/master/SearchEngine

<!-- For the query expansion: 
pip install vocabulary user

import nltk
nltk.download('wordnet') -->
