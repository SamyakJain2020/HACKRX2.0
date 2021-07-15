from autoscraper import AutoScraper
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import string
import csv
url=["https://www.bajajfinserv.in/health-insurance",
    "https://www.bajajfinserv.in/life-insurance",
    "https://www.bajajfinserv.in/motor-insurance",
    "https://www.bajajfinserv.in/home-insurance",
    "https://www.bajajfinserv.in/travel-insurance",
    "https://www.bajajfinserv.in/two-wheeler-insurance",
    ]

def getNgrams(content, n):
    content = bytes(content, 'UTF-8')
    content = content.decode('ascii', 'ignore')
    content = content.split(' ')
    output = []
    for i in range(len(content)-n+1):
        if(content[i:i+n]!=['','']):
            output.append(content[i:i+n])
    return output

def isCommon(ngram):
    commonWords = ['the', 'be', 'and', 'of', 'a', 'in', 'is', 'to', 'have', 'it', 'i', 'that', 'for', 'you', 'he', 'with', 
        'on', 'do', 'say', 'this', 'they', 'is', 'an', 'at', 'but', 'we', 'his', 'from', 'that', 'not', 'by', 'she', 'or',
        'as', 'go', 'their', 'can', 'get', 'her', 'all', 'my', 'make', 'about', 'know', 'will','as', 'up', 'one', 'time', 
        'has', 'been', 'there', 'year', 'so', 'think', 'when', 'which', 'them', 'some', 'me', 'people','find', 'here', 'thing', 'give',
        'take', 'out', 'into', 'just', 'see', 'him', 'your', 'come', 'could', 'now', 'than', 'like', 'other', 'how', 'then', 'its',
        'our', 'two', 'more', 'these', 'want', 'way', 'look', 'first', 'also', 'new', 'because', 'day', 'more', 'use', 'no', 'man',
         'many', 'well', 'rs']
    if ngram in commonWords:
        return True
    return False

# def getNgramsFromSentence(content, n):
#     output = []
#     for i in range(len(content)-n+1):
#         if not isCommon(content[i:i+n]):
#             output.append(content[i:i+n])
#     return output

def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub(' +', ' ', text)
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

def clean_text_round2(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\r', '', text)
    text = re.sub('\t', '', text)
    text = re.sub('\n|[[\d+\]]', ' ', text)
    w = text.split()
    r  = [word for word in w if not isCommon(word)]
    text = ' '.join(r)
    return text


r = requests.get(url[0])		# r variable has all the HTML code
htmlContent = r.content	# r returns response so if we want the code we write r.content
soup = BeautifulSoup(r.content, 'html.parser') #HTML TREE Created

table = soup.find('div', attrs = {'class':'col-lg-9 col-md-9 col-sm-12 col-xs-12'}) 

list=[]
for row in table.findAll('p'):
    list.append(row.text)
for row in table.findAll('h2'):
    list.append(row.text)
        
for i in range(len(list)):
    list[i]=clean_text_round2(clean_text_round1(list[i]))

# print(list)

fin=[]
for i in range(len(list)):
    fin.append(getNgrams(list[i],1))

# print(fin[0])

final_scrapped=Counter()
# Counter is for hashing 


newNgrams=[]
ngrams = Counter()
ngrams_list = []
for i in range(len(fin)):   
    newNgrams = [' '.join(ngram) for ngram in fin[i]]
    ngrams_list.extend(newNgrams)
    ngrams.update(newNgrams)

print(type(ngrams))

with open('test1.csv','w',encoding='utf-8',newline='') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(ngrams)
    for key, value in ngrams.items():
        writer.writerow([key] + [value])
print("DONE")



# line 86: change second parameter to 1,2,3 to get ngrams length
# line 67: change index of list to update new url


# https://cse.google.com/cse?cx=d5a7de292dc3f1e3f


# <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' acoTextHeadLeft ')]
# FOR HEALTH INSURANCE
# section class="v1_alltextpage"
#     div class="container"
#         div class="row"
#             div class="col-lg-9 col-md-9 col-sm-12 col-xs-12"
#                 div class="v1_leftsidebox playBtnPrent acoAroOnly"
#                     div class="acoTextHeadLeft"    
#                         <h2>heading
#                     div class="v1_boxinsidepadd"
#                         <p> para
#                         <ul> class= "v1_dotDiscriptionUl"  
#                             <li>