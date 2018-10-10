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
import sys


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

def snap_shot(csv_file) -> dict:
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
    csv_file = open(sys.argv[1],"rt")
    snap = snap_shot(csv_file)

    