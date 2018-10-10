#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 19:10:27 2018

@author: miaaltieri

This script returns the slice of the users post history 
"""


import sys, csv
import string
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

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


# returns an array of length k, each slice will contain the users posts from an
# a specific time period. Each slice has the same length time period
# requires k, start time, end time, and a hash time containing all user posts
# where the key is the time of post.
# note: time is measured on a monthly basis 
def equal_time_slices(k, start_time, end_time, user_posts):
    quantum = int((end_time - start_time) / k)
    time_slice = [None] * k
    i = 0
    # loop through all posts
    for period in range (start_time, end_time, quantum):
        text = []
        # loop through all posts within quantum
        for j in range (period,period+quantum):
            if j in user_posts:
                text.extend(user_posts[j])
        time_slice[i] = text  
        i+=1
    return time_slice
    

# gathers all posts from a specific user, cleans up the the text from that user
# and stores text by time of post, also saves earliest time and save latest 
# time of user post, then utilzes equal_time_slices to slice up the users 
# information.
# requires csv of all posts, a specified  user, and the number of slices(k)
def user_posts_time_slice (k, user_name, all_posts):
    user_posts = {}
    start_time = 99
    end_time = 0
    reader = csv.reader(all_posts)
    for idx,post in enumerate(reader):
        date = (post[2]).split()
        time = (int(date[5])%2011)*12
        time = time + convert_month(date[1])
        text = clean_text(post[5])
        if user_name == post[0]:
            if time < start_time:
                start_time = time
            if time > end_time:
                end_time = time
            if time in user_posts:
                user_posts[time] = user_posts[time] + text
            else:
                user_posts[time] = text
    
    return equal_time_slices(k, start_time, end_time, user_posts)
    
if __name__ == "__main__":
    #Expect first argument to sys.argv is a csv filename
    csv_file = open(sys.argv[1],"rt")
    print(user_posts_time_slice(5,"db02dbe091e6e78068f37f4f9f6a1ef321ab9916",csv_file))
