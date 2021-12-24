import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt# Define a function to plot word cloud
from wordcloud import WordCloud, STOPWORDS# Generate word cloud


#wordlist=""
punc = '''!()--—[]{};:'",<>./?@#$%^&*_~'''
lengthofcounter=0
AllTheWords=""


#Create Listing for the sites used
filterwords=[]
filterW = open("filterwords.txt", "r")
for i in filterW:
    filterwords.append(i.strip())
filterW.close()

#loop to determine the length of filterwords
for l in filterwords:
    lengthofcounter=lengthofcounter+1

#Eric's loop to get the name of the news site
def get_source(url):
    url = urllib.parse.urlparse(url).netloc
    source = url.split('.')
    if len(source) == 2:
        source = source[0]
    elif len(source) == 3:
        source = source[1]
    elif len(source) == 4:
        source = source[1]
    return source

#The main function that scrapes the news sites and currently also does some filtering
def scrapeTheNews(site):
    counter=0
    newline = ""
    wordlist = ""
    the_page = requests.get(site)
    soup=BeautifulSoup(the_page.content, "xml")
    get_tag=soup.find_all('description')

    for i in get_tag:
        line=i.get_text()
        wordlist=wordlist+line

        #This is supposed to get rid of punctuation but it doesn't work yet....
        for ii in line:
            if ii in punc:
                ii=""
                newline=newline+ii
            else:
                newline=newline+ii

    #the word filtering loop
    while counter<lengthofcounter:
            for i in wordlist.split():
                if i == filterwords[counter]:
                    i=""
            counter=counter+1
    return wordlist

#Create Listing for the sites used
sitesUsed=""
sitesDoc = open("sites.txt", "r")
for i in sitesDoc:
    AllTheWords=AllTheWords+scrapeTheNews(i)
    sitesUsed=sitesUsed+'<p>'+get_source(i)+"</p>"
sitesDoc.close()

#Wordcloud and matplot
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off");

#Wordcloud and matplot
wordcloud = WordCloud(width= 3000, height = 4000, max_words=50, random_state=1, background_color='DarkSeaGreen', colormap='prism', collocations=False, stopwords = STOPWORDS).generate(AllTheWords)# Plot
plot_cloud(wordcloud)

#save image toggle
#wordcloud.to_file("wordcloud.png")
wordcloud.to_file("/var/www/html/wordcloud.png")


#local vs server toggle
#f = open("index.html", "w")
f = open("/var/www/html/index.html", "w")

#open static html files
htmlheader=open('htmlheader.html', 'r')
htmlfooter=open('htmlfooter.html', 'r')

#write the index.html page NOTE: THIS IS VERY MESSY. I'm close divving the dropdown in here and other messes
f.write(htmlheader.read()+str(sitesUsed)+"</div></div>"+'<div class="container">'+' <img src="wordcloud.png" alt="wordcloud" width=100%>'+"<div>"+"</br></br>"+htmlfooter.read())

#close files
htmlheader.close()
htmlfooter.close()
f.close()