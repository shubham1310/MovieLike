import json
import time
import csv
import metapy
import operator

class Searcher:
    """
    Wraps the MeTA search engine and its rankers.
    """
    movies = []
    praiseWords = []
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
        nametorating={}
        nametogenre={}
        nametotime={}
        with open('../ScrapyIMDB/data/movie_list.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                if unicode(row[-1][-1], 'utf-8').isnumeric():
                    if row[0]=='' or not(row[0].replace('.','',1).isdigit()):
                        pass
                    else:
                        nametoid[row[-2]]=row[-1]
                        nametorating[row[-2]] = row[0]
                        nametogenre[row[-2]] = row[1].replace(',',', ')
                        nametotime[row[-2]] = row[2]
        self.nametoid =nametoid
        self.nametorating = nametorating
        self.nametogenre = nametogenre
        self.nametotime = nametotime


        title=[]
        with open("./reviews/titles.dat", "r") as ins:
            for line in ins:
                title.append(line)
        self.titles=title

        c = [["acceptable", "decent", "honorable", "satisfactory"], ["amazing", "awesome", "excellent", "exceptional", "fantastic", "great", "super", "superb", "superior", "terrific", "remarkable", "marvelous", "splendid", "wonderful", "worthy", "genius", "premium", "stupendous",], ["good", "nice", "pleased", "pleasing"], ["admirable", "agreeable", "commendable", "favorable", "gratifying", "satisfying"]]
        self.praiseWords = {}
        for i in c:
            for k in range(len(i)):
                self.praiseWords[i[k]]=i[:k]+i[min(k+1,len(i)):]


    def expandQuery(self,query):
        newQuery = "";
        # print self.praiseWords.keys()
        for word in query.split(" "):
            if word in self.praiseWords.keys():
                for syn in self.praiseWords[word]:
                    newQuery += syn + " ";

            newQuery += word + " "

        print newQuery;


    def search(self, request):
        """
        Accept a JSON request and run the provided query with the specified
        ranker.
        """
        ranker_id = request['ranker']
        queries = request['query'].split(',');
        try:
            ranker = getattr(metapy.index, ranker_id)()
        except:
            print("Couldn't make '{}' ranker, using default.".format(ranker_id))
            ranker = self.default_ranker

        results = {}
        for q in queries:

            start = time.time()
            query = metapy.index.Document()
            self.expandQuery(q)
            query.content(q)
            
            response = {'query': request['query'], 'results': []} 
        
            for result in ranker.score(self.idx, query):
                if results.has_key(result[0]):
                    results[result[0]] += result[1];
                else:
                    results[result[0]] = result[1]

        for k in results:
            results[k] = results[k]/len(queries);

        sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
        for result in sorted_results:
            # print ('http://www.imdb.com/title/' + self.nametoid[self.movies[int(result[0])].strip()])
            response['results'].append({
                'score': float(result[1]),
                'name': self.movies[int(result[0])],
                'path' : self.nametoid[self.movies[int(result[0])].strip()],
                'title': self.titles[int(result[0])],
                'rating': self.nametorating[self.movies[int(result[0])].strip()],
                'genre': self.nametogenre[self.movies[int(result[0])].strip()],
                'time': self.nametotime[self.movies[int(result[0])].strip()],
                'namestrip' : self.movies[int(result[0])].replace(' ','').replace(':','').replace('/',''),
                # 'path': self.idx.doc_path(result[0])
            })
        response['elapsed_time'] = time.time() - start
        return json.dumps(response, indent=2)

