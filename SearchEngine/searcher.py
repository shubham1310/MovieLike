import json
import time
import csv
import metapy

class Searcher:
    """
    Wraps the MeTA search engine and its rankers.
    """
    movies = []
    def __init__(self, cfg):
        """
        Create/load a MeTA inverted index based on the provided config file and
        set the default ranking algorithm to Okapi BM25.
        """
        self.idx = metapy.index.make_inverted_index(cfg)
        self.default_ranker = metapy.index.OkapiBM25()
        with open("reviews/movienames.txt", "r") as ins:
            for line in ins:
                self.movies.append(line)

        nametoid={}
        with open('../ScrapyIMDB/scrapyIMDB/data/movie_list.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                if unicode(row[-1][-1], 'utf-8').isnumeric():
                    if row[0]=='' or not(row[0].replace('.','',1).isdigit()):
                        pass
                    else:
                        nametoid[row[-2]]=row[-1]
        self.nametoid =nametoid

        title=[]
        with open("../titles.dat", "r") as ins:
            for line in ins:
                title.append(line)
        self.titles=title


    def search(self, request):
        """
        Accept a JSON request and run the provided query with the specified
        ranker.
        """
        start = time.time()
        query = metapy.index.Document()
        query.content(request['query'])
        ranker_id = request['ranker']
        try:
            ranker = getattr(metapy.index, ranker_id)()
        except:
            print("Couldn't make '{}' ranker, using default.".format(ranker_id))
            ranker = self.default_ranker
        response = {'query': request['query'], 'results': []} 
        for result in ranker.score(self.idx, query):
            print self.movies
            print int(result[0])
            print ('http://www.imdb.com/title/' + self.nametoid[self.movies[int(result[0])].strip()])
            response['results'].append({
                'score': float(result[1]),
                'name': self.movies[int(result[0])],
                'path' : self.nametoid[self.movies[int(result[0])].strip()],
                'title': self.titles[int(result[0])],
                # 'path': self.idx.doc_path(result[0])
            })
        response['elapsed_time'] = time.time() - start
        return json.dumps(response, indent=2)

