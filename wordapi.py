import unirest
import json

def runcall(pos):
    response = unirest.get("https://wordsapiv1.p.mashape.com/words/?partOfSpeech=verb&random=true",
      headers={
        "X-Mashape-Key": "MbJW6EIVQLmshESVsKmj3y1JaPkDp1EcR9FjsnSXPngMMiAFTd",
        "Accept": "application/json"
      }
    )
    return response.body['word']

def findword(arr):
    words_arr=[]
    for i in arr:
        if i == 'noun' or i == 'verb' or i=='adjective' or i=='adverb':
            words_arr.append(runcall(i))
        elif i == 'proper noun':
            words_arr.append(runcall('noun'))
        elif i=='plural noun':
            words_arr.append(runcall('noun')+'s')
        elif i=='verb ending with ing':
            words_arr.append(runcall('verb')+'ing')
        elif i=='verb past tense':
            words_arr.append(runcall('verb')+'ed')
        else:
            words_arr.append(runcall('noun'))
    return words_arr
