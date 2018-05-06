
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import scipy.stats as sts
import re
from bs4 import BeautifulSoup
import urllib.request

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Custom User Agent 1.0',
        'From': 'shubham9@illinois.edu' 
    }
)
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()


# In[ ]:


def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
import csv
ids=[]
idstoname={}
with open('./ScrapyIMDB/data/movie_list.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        if row[-1][-1].isnumeric():
            if row[0]=='' or not(row[0].replace('.','',1).isdigit()):
                pass
            else:
                ids.append(row[-1]) #ids for links in movies
                idstoname[row[-1]]=row[-2] #name of the movie 
ids = list(set(ids))


# In[ ]:


N=1000
#This gets all the reviews for all the movies looks at different possible sorting methods (in sort)
# ids=['tt2488496']
reviewfile = open('./SearchEngine/reviews/reviews.dat','w')
moviename= open('./SearchEngine/reviews/movienames.txt','w')
count=0
for k in ids[:N]:
    print(count,k)
    count+=1
    url = 'http://www.imdb.com/title/'+str(k)+'/reviews'
    sort =['?sort=helpfulnessScore','?sort=submissionDate','?sort=totalVotes','?sort=reviewVolume','?sort=userRating']
    direc =['&dir=desc','&dir=asc']
    data=[]
    user=[]
    maintext=''
    for i in sort:
        for j in direc:
            r = requests.get(url + i+j, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            listing = soup.find(class_='lister')
            if listing==None:
                continue
            reviews = listing.find_all(class_='lister-item-content')
            for row in reviews:
                if str(row.find(class_='display-name-date')).split('tt_urv">')[1].split('</')[0] in user:
                    break
                else: #ensures we don't include the same review twice
                    user.append(str(row.find(class_='display-name-date')).split('tt_urv">')[1].split('</')[0])
                    
                if str(row).find('text show-more__control')>=0: #add text of review
                    text =str(row.find(class_='text show-more__control')).split('<div class="text show-more__control">')[1].split('</div>')[0]
                else:
                    print('doesnt exist')
                    text=''
                    
                if str(row.find(class_='ipl-ratings-bar')).find('<span>') >=0: #rating of the review
                    rating = int(str(row.find(class_='ipl-ratings-bar')).split('<span>')[1].split('</span>')[0])
                else:
                    rating=-1
                
                title = str(row.find(class_='title')).split('>')[1].split('<')[0]
                htmlTags = re.compile('<.*?>') #cleaning up html
                text = re.sub(htmlTags, ' ', text)
                title = re.sub(htmlTags, ' ', title)
                maintext+= title +' ' + text # + '\n' 
    maintext = maintext.replace("\n", " ")
    maintext = maintext.replace("  ", " ")
    maintext=removeNonAscii(maintext) 
    words = word_tokenize(maintext) #stop word removal
    line =""
    for w in words:
        line+=ps.stem(w) +" "
    reviewfile.write("%s\n"%line)
    moviename.write("%s\n"%idstoname[k])
reviewfile.close()
moviename.close()


# In[ ]:


#saves plot of the movies 
# ids=['tt2488496']
count=0
title= open('./SearchEngine/reviews/titles.dat','w')
for k in ids[:N]:
    print(count,k)
    count+=1
    url = 'http://www.imdb.com/title/'+str(k)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    listing = soup.find(class_='summary_text')
    maintext = str(listing).split('>')[1].split('<')[0]
    maintext = maintext.replace("\n", " ")
    maintext = (maintext.replace("  ", " ")).strip()
    title.write("%s\n"%maintext)
title.close()


# In[ ]:


#saves image posters of the movies 
count=0
for k in ids[:N]:
    print(count,k)
    count+=1
    url = 'http://www.imdb.com/title/'+str(k)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    listing = soup.find(class_='poster')
    if not(listing==None):
        link = str(listing).split('src=')[1].split('"')[1]
        urllib.request.urlretrieve(link, './SearchEngine/static/search/image/' + idstoname[k].replace(' ','').replace(':','').replace('/','')+".jpg")

        


# In[ ]:


# b = removeNonAscii(b)
# f = open('stemreview.dat','w')
# for i in b.split('\n'):
#     words = word_tokenize(i)
#     line =""
#     for w in words:
#         # print(ps.stem(w))
#         line+=ps.stem(w) +" "
#     f.write(line +'\n')

