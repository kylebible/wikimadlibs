# -*- coding: utf-8 -*-
import requests
import json
from unidecode import unidecode
import re
import wordapi

def validatesearch(search):
    response = requests.get('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&indexpageids=&titles='+search)
    page_id = response.json()['query']['pageids']
    if page_id[0]=='-1':
        search_response=requests.get('https://en.wikipedia.org/w/api.php?action=opensearch&search='+search+'&limit=1&namespace=0&format=json')
        didyoumean= raw_input('Did you mean '+search_response.json()[1][0]+'? y/n >>>>')
        if didyoumean=='y':
            search=search_response.json()[1][0]
            return requests.get('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&indexpageids=&titles='+search)
        elif didyoumean=='n':
            return validatesearch(raw_input('Try someone else, or a different spelling! >>>>'))
    elif not response.json()['query']['pages'][page_id[0]]['extract']:
        return validatesearch(raw_input('Try someone else, or a different spelling! >>>>'))
    else:
        return response

response = validatesearch(raw_input('Type a celebrity to madLib! >>>>'))
page_id = response.json()['query']['pageids']

name = response.json()['query']['pages'][page_id[0]]['title']
paragraph = response.json()['query']['pages'][page_id[0]]['extract']
# print page_id, name, unidecode(paragraph)
encoded_paragraph= unidecode(name+" is a"+paragraph.split(' is a', 1)[1]).splitlines()[0]
madlibbed_response = requests.get('http://libberfy.herokuapp.com/?blanks=10&q='+encoded_paragraph)
madlibbed_str = unidecode(madlibbed_response.json()['madlib'])
blank_arr = re.findall(r'\<(.*?)\>', madlibbed_str)
for i in range(0,len(blank_arr)):
    blank_arr[i]=(blank_arr[i].replace("_"," "))

replace_arr = wordapi.findword(blank_arr)

# replace_arr = []


words_added = madlibbed_str

# for i in range(0,10):
#     replace_arr.append(raw_input('Type a '+blank_arr[i]+' >>>'))

for i in range(0,len(replace_arr)):
    words_added=re.sub(r'\<(.*?)\>', replace_arr[i], words_added, 1)



print words_added
