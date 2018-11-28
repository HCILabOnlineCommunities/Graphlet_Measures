#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 21:16:30 2018

@author: miaaltieri
"""

import string, nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

path = '/Users/miaaltieri/Research_Data/Test_Data'

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


# cleans the text to remove punctuation, stopwords, etc
def clean_text(text):
    text = text.translate(remove_punctuation_map).lower()
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    return filtered_sentence[0:30]

def convert_month(month) -> int:
    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]
    for i,m in enumerate(months):
        if m == month:
            return i+1

# returns a dictionary where the key is the subgraph and the value is its
# progressive rating
def progressiveness_wi_commun(k, snap_shots, path_to_comm, path_to_comm_graphlets):
    progressive_ratings = {}
    
    #Load in the graph object
    comm_graph = None
    with open( path_to_comm,"rb") as f_p:
        comm_graph = pickle.load(f_p, encoding='latin1')
    #Load in the graphlet list
    comm_graphlets = None
    with open(path_to_comm_graphlets,"rb") as f_p:
        comm_graphlets = pickle.load(f_p, encoding='latin1')
        
    #Iterate through graphlet list
    for graphlet in comm_graphlets:
        # how should I grab the post id? 
        name = ""
        total_text = ""
        time = 0
        count = 0
        
        #Grab the subgraph
        subg = comm_graph.subgraph(graphlet)
        #Iterate through edges
        for edge in subg.edges:
            for post in edge["post_reply_data"]:
                    text = post["Original_text"]
                    date = post["reply_date"].split()
                    time = time + (int(date[5])%2011)*12 + convert_month(date[1])
                    total_text = total_text+" "+text.replace(post["Original_post_text"],"");
                    count+=1
        # find average date?
        time = time/count 
        total_text = clean_text(total_text)
        progressive_ratings[name]=ling_prog(k, total_text, time, snap_shots)