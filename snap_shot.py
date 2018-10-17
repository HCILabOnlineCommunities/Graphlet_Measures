# -*- coding: utf-8 -*-
"""
Spyder Editor

This script file will take a snapshot of a csv full of text
and divide up the text in the csv based on the month and year
we assume to be analyzing no earlier than 2011.
"""

# -*- coding: utf-8 -*-
""" 
Created on Mon Oct 6 11:45:46 2018
@author: Mia Altieri
"""

import string
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import csv
# import sys
import os
import pickle

userID = "your id here"

path = '/Users/userID/Research_Data/Test_Data/Comm_Test_Data'

remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

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

#comm_graph.edges[edge]["post_reply_data"][list_index]["Original_text"]
def snap_shot_graph(graphlets_path) -> dict:
    time_line = {}
    
    a = [0,1,2,3,4]
    i = 4
    print(a[i])
    for elem in a:
        print(elem)
    
    
    # loop through each pickle file in folder
    for filename in os.listdir(graphlets_path):
        print(filename)
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
                time = (int(date[5])%2011)*12
                time = time + convert_month(date[1])
                text = text.replace(post["Original_Title"],"");
                text = clean_text(text)
                if time in time_line:
                    time_line[time] = time_line[time] + text
                else:
                    time_line[time] = text
    return time_line


def snap_shot_csv(csv_file) -> dict:
    time_line = {}
    reader = csv.reader(csv_file)
    for idx,row in enumerate(reader):
        date = (row[2]).split()
        time = (int(date[5])%2011)*12
        time = time + convert_month(date[1])
        content = row[5].replace(row[4],"");
        text = clean_text(content)
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
    #snap = snap_shot_csv(csv_file)
    
    #Load in the graph object

    snap = snap_shot_graph(path)
    print (snap)
    
    #with open(os.path.join(path, "snap_shot.pickle"),'wb') as out:
    #   pickle.dump(prog,out)
    
    

    
