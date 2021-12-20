
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from collections import Counter

import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


wordlist=[]
punc = '''!()--—[]{};:'",<>./?@#$%^&*_~'''
lengthofcounter=0
AllTheWords=[]

#change this to be from a file
filterwords =["New","The","York","Times","A",
"in","to", "the","was","when","his","News","for","I","where","of","on", "+", "and","a","by","with","is","as","be","after","are","at","or","&","|","from","Is","With","but","has","than","an","your","Do","But","it",">","which","that","have","will","they","That","can","Other","their","how","you","could","my","feedback!","hour","about"]

for l in filterwords:
		lengthofcounter=lengthofcounter+1


def scrapeTheNews(site):

	counter=0
	newline = ""

#	thislist = []
	the_page = requests.get(site)
	soup=BeautifulSoup(the_page.content, "xml")
	get_tag=soup.find_all('item')



	#Get rid of punctuation
	for i in get_tag:
		line=i.description.get_text().strip()
		for ii in line:
			if ii in punc:
				ii=""
				newline=newline+ii
			

			else:
				newline=newline+ii

		for word in line.split():
			wordlist.append(word)
	

	#the word filtering loop
	while counter<lengthofcounter:
			for i in wordlist:
				if i == filterwords[counter]:
					wordlist.remove(i)
			counter=counter+1
	return wordlist

#Create Listing for the sites used
sitesUsed=""
sitesDoc = open("sites.txt", "r")
for i in sitesDoc:
	AllTheWords=AllTheWords+(scrapeTheNews(i))
	sitesUsed=sitesUsed+"<p>"+i+"</p>"


topWords=Counter(AllTheWords).most_common(100)
sitesDoc.close()

#local vs server toggle
#f = open("index.html", "w")
f = open("/var/www/html/index.html", "w")


theDoc="<h1>Top 100 words used in headlines</h1></br><h2>the headlines from the following sites are scraped every hour and sorted for the top 100 words.</h2>"


f.write(theDoc+sitesUsed+"</br>"+"<h2>Output Below as Shown</h2></br>"+"<p>"+str(topWords)+"</p>")
f.close()




