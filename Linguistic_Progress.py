#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues Oct  8 18:48:33 2018

@author: miaaltieri

This script computes the linguistic progressiveness of a single post compared 
to the 'k' months prior and later

"""

import sys, csv
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from sklearn.metrics import jaccard_similarity_score

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


# cleans the text to remove punctuation, stopwords, etc
def clean_text(text):
    text = text.translate(remove_punctuation_map).lower()
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    return filtered_sentence[0:30]

# then puts the text into an array
def jaccard_similarity(text1, text2):
    return jaccard_similarity_score(clean_text(text1),clean_text(text2))

# excpets that post_content and snap_shots
def ling_prog (k, post_content, post_time, snap_shots) -> int:
    entropy_min = 0
    index_min = 0
    for i in range (post_time-k-1, post_time+k+1):
        if i == post_time:
            continue
        if i not in snap_shots: 
            continue
        snapshot_i = snap_shots[i]
        entropy = cosine_sim(" ".join(snapshot_i), " ".join(post_content))
        if entropy > entropy_min:
            entropy_min = entropy
            index_min = i
    return index_min


def convert_month(month) -> int:
    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]
    for i,m in enumerate(months):
        if m == month:
            return i+1

def snap_shot(csv_file) -> dict:
    time_line = {}
    reader = csv.reader(csv_file)
    for idx,row in enumerate(reader):
        date = (row[2]).split()
        time = (int(date[5])%2011)*12
        time = time + convert_month(date[1])
        text = clean_text(row[5])
        if time in time_line:
            time_line[time] = time_line[time] + text
        else:
            time_line[time] = text
    return time_line

if __name__ == "__main__":
    #Expect first argument to sys.argv is a csv filename
    #This csv file is expected to have headers and a column
    #header named "text"
    csv_file = open(sys.argv[1],"rt")
    snap = snap_shot(csv_file)
    post =  ['friday', 'live', 'reviews', 'recorded', 'sessions', 'ibm', 'confidential', 'please', 'shareevangelize', 'internally', 'share', 'customers', 'order', 'promote', 'awareness', 'actively', 'developed', 'traditionally', 'held', 'routine', 'live', 'reviews', 'new', 'features', 'purpose', 'live', 'review', 'present', 'new', 'capability'] 
    print (ling_prog(12, post, 11, snap))


    
# -*- coding: utf-8 -*-

