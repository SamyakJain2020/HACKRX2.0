import requests
from bs4 import BeautifulSoup
import re
import string
import pandas as pd
from collections import Counter

def clean_text_round1(s):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    for i in range(len(s)):
        s[i] = s[i].lower()
        s[i] = re.sub(' +', ' ', s[i])
        s[i] = re.sub('\[.*?\]', '', s[i])
        s[i] = re.sub('[%s]' % re.escape(string.punctuation), '', s[i])
        # s[i] = re.sub('\w*\d\w*', '', s[i])
    return s 

def clean_text_round2(s):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    for i in range(len(s)):
        s[i] = re.sub('[‘’“”…]', '', s[i])
        s[i] = re.sub('\n', '', s[i])
        s[i] = re.sub('\r', '', s[i])
        s[i] = re.sub('\t', '', s[i])
    return s

def get_FAQ_question(url):
    website = requests.get(url)		
    htmlContent = website.content	
    soup = BeautifulSoup(website.content, 'lxml') 
    questions = soup.find_all('h3', attrs = {"itemprop":"name"})
    questions1 = soup.find_all('h2', attrs = {"itemprop":"name"})
    questions=questions+(questions1)
    for i in range(len(questions)):
       questions[i]=questions[i].get_text()
    return (questions)

def get_FAQ_answers(url):
    website = requests.get(url)		
    htmlContent = website.content	
    soup = BeautifulSoup(website.content, 'lxml') 
    answers = soup.find_all('div'  , attrs = {"itemprop":"text"})
    for i in range(len(answers)):
        answers[i]=answers[i].get_text()
    return answers

def get_data(url):
    website = requests.get(url)		
    htmlContent = website.content	
    soup = BeautifulSoup(website.content, 'lxml') 
    data = soup.find_all('p'  , attrs = {"class":"v1_descperg"})
    data1=soup.find_all('p'  , attrs = {"style":"margin-top:-25px;"})
    data2=soup.find_all('ul'  , attrs = {"class":"fNbList"})
    data3=soup.find_all('p'  , attrs = {"class":"eliPera"})
    data=data+data1+data2+data3

    for i in range(len(data)):
        data[i]=data[i].get_text()
    return data

loan_url=[
    ["https://www.bajajfinserv.in/personal-loan","https://www.bajajfinserv.in/personal-loan-eligibility-calculator"],
    ["https://www.bajajfinserv.in/home-loan",""],
    ["https://www.bajajfinserv.in/business-loan",""],
    ["https://www.bajajfinserv.in/personal-loan-for-self-employed",""],
    ["https://www.bajajfinserv.in/two-and-three-wheeler-loan",""],
    ["https://www.bajajfinserv.in/loan-against-property",""],
    ["https://www.bajajfinserv.in/loan-against-shares",""]
]

# for u in range(1):
raw_answers=clean_text_round2(get_FAQ_answers(loan_url[0][0]))
raw_question=clean_text_round2(get_FAQ_question(loan_url[0][0]))
raw_data=get_data(loan_url[6][0])

clean_answers=clean_text_round2(clean_text_round1(raw_answers))
clean_question=clean_text_round2(clean_text_round1(raw_question))
clean_data=clean_text_round2(clean_text_round1(raw_data))
for i in clean_data:
    print (i+"\n")
# pd.DataFrame({'QUESTIONS': raw_question, 'ANSWERS': raw_answers, }, 
# columns=['QUESTIONS','ANSWERS']).to_csv('file1.csv', index=False)
