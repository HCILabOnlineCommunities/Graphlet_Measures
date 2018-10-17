#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues Oct  8 18:48:33 2018

@author: miaaltieri

This script computes the linguistic progressiveness of a single post compared 
to the 'k' months prior and later

"""

import sys, csv, os
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import pickle
from sklearn.metrics import jaccard_similarity_score

userID = "your id here"

path_graphs = '/Users/'+userID+'/Research_Data/Test_Data/Comm_Test_Data'
path_graphlets = '/Users/'+userID+'/Research_Data/Test_Data/Four_Cliques_Test_Data'
path = "~/"
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
    for i in range (post_time-k, post_time+k+1):
        if i == post_time:
            continue
        if i not in snap_shots: 
            continue
        snapshot_i = snap_shots[i]
        entropy = cosine_sim(" ".join(snapshot_i), " ".join(post_content))
        if entropy > entropy_min:
            entropy_min = entropy
            index_min = i
    return index_min-post_time


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
    
    least = 2010
    #Iterate through graphlet list
    # loop through each pickle file in folder
    for filename in os.listdir(path_to_comm_graphlets): 
        print(filename)
        total_text = []
        time = 0
        count = 0
        subgraph_name = filename.split('_')[0]
        graphlets = None
        comm_graph = None
        #Load in the graphlets
        with open(os.path.join(path_to_comm_graphlets,filename),"rb") as f_p:
            graphlets = pickle.load(f_p, encoding='latin1')
        
        #Load in the graph object
        with open(os.path.join(path_to_comm,subgraph_name+"_graph.pickle"),"rb") as f_p:
            comm_graph = pickle.load(f_p, encoding='latin1')
        
        # go through the list of the graphlets
        for graphlet in graphlets:
            #Grab the subgraph
            subg = comm_graph.subgraph(graphlet)
        
            #Iterate through edges in subgraph
            for edge in subg.edges:
                #loop through each post_reply pair in the edge (i.e. looping through list_index)
                for post in comm_graph.edges[edge]["post_reply_data"]: 
                    text = post["Original_Text"]
                    date = post["Reply_Date"].split()
                    time = time + (int(date[5])%2009)*12 + convert_month(date[1])
                    text = text.replace(post["Original_Title"],"")
                    total_text.extend(clean_text(text)) ;
                    count+=1
            
        # now find ling_prog of the graphlet_list
        if count != 0:
            time = (int)(time/count) 
            rating = ling_prog(k, total_text, time, snap_shots)
            progressive_ratings[subgraph_name] = rating
            print(time, rating)
        else:
            print("count = 0")
            
    print(least)
    return progressive_ratings

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

#comm_graph.edges[edge]["post_reply_data"][list_index]["Original_text"]
def snap_shot_graph(graphlets_path) -> dict:
    time_line = {}
    # loop through each pickle file in folder
    for filename in os.listdir(graphlets_path):
        #unpickle the file
        comm_graph = None
        with open(os.path.join(graphlets_path,filename,),"rb") as f_p:
            comm_graph = pickle.load(f_p, encoding='latin1')
        #loop through each edge in graph (i.e looping through edges)
        for edge in comm_graph.edges:
            #loop through each  post_reply pair in the edge (i.e. looping through list_index)
            for post in comm_graph.edges[edge]["post_reply_data"]: 
                text = post["Original_Text"]
                date = post["Reply_Date"].split()
                time = (int(date[5])%2009)*12
                time = time + convert_month(date[1])
                text = text.replace(post["Original_Title"],"");
                text = clean_text(text)
                if time in time_line:
                    time_line[time] = time_line[time] + text
                else:
                    time_line[time] = text
    return time_line

if __name__ == "__main__":
    #Expect first argument to sys.argv is a csv filename
    #This csv file is expected to have headers and a column
    #header named "text"
    #csv_file = open(sys.argv[1],"rt")
    #snap = snap_shot(csv_file)
    #post =  ['friday', 'live', 'reviews', 'recorded', 'sessions', 'ibm', 'confidential', 'please', 'shareevangelize', 'internally', 'share', 'customers', 'order', 'promote', 'awareness', 'actively', 'developed', 'traditionally', 'held', 'routine', 'live', 'reviews', 'new', 'features', 'purpose', 'live', 'review', 'present', 'new', 'capability'] 
    #print (ling_prog(12, post, 11, snap))
    snap_shots = snap_shot_graph(path_graphs)
    prog = progressiveness_wi_commun(12, snap_shots, path_graphs, path_graphlets)
    for k,v in prog.items():
        print(k,v)
    #with open(os.path.join(path, "graphlet_progression.pickle"),'wb') as out:
    #   pickle.dump(prog,out)
    
# -*- coding: utf-8 -*-

