# ScrapyIMDB


Crawl IMDB user's review

All runnable scripts are in: [scripts](script)

Running steps:

[crawl_movie_list.sh](script/crawl_movie_list.sh) : execute module [movies_spider](scrapyIMDB/spiders/movies_spider.py), crawl a list of movie(& its information) from the link      `http://www.imdb.com/search/title?year={year},{year}&title_type=feature&sort=num_votes,desc`