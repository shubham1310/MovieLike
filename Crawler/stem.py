import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()
a = open('reviews.dat','r')
b = a.read()
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

b = removeNonAscii(b)
f = open('stemreview.dat','w')
for i in b.split('\n'):
	words = word_tokenize(i)
	line =""
	for w in words:
		# print(ps.stem(w))
		line+=ps.stem(w) +" "
	f.write(line +'\n')