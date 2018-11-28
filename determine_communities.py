#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 13:26:58 2018

@author: miaaltieri

Given a list of csv communities, this python script will print the top ten
values in a dictionary where it is of the format:
    (key) - value
    (commun_Name) - (# of different months, time period)

this will be useful because we can see which dictionaries will be useful for 
our snapshot analysis, ideally we want one with a ton of months with a high 
density, (i.e. not spread out over a huge time period) basically
    # of different months = time period 
    and both > 24 
    
is ideal. 
"""

import csv
import itertools
import operator
import os
import pickle
import sys

csv.field_size_limit(sys.maxsize)
least = 2006
communities = "/Users/miaaltieri/Research_Data/Comm_Text"
result_path = "/Users/miaaltieri/Research_Data/Results/top_100_commun"


def convert_month(month) -> int:
    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]
    for i,m in enumerate(months):
        if m == month:
            return i+1


# don't foreget to check if wiki present
def snap_shot_csv(csv_file):
    global least
    time_line = {}
    reader = csv.reader(csv_file)
    for idx,row in enumerate(reader):
        if row[3] == 'Wiki' or row[3] == 'Idea' or row[3] == 'IdeaCmt':
            continue
        date = (row[2]).split()
        if int(date[5]) <  2006:
            print(least,"=============")
            least = int(date[5])
        if int(date[5]) == 1969:
            continue
        time = (int(date[5])%2006)*12
        time = time + convert_month(date[1])
        if time not in time_line:
            time_line[time] = 0
        time_line[time] += 1
    
    if len(time_line) < 1 :
        return (len(time_line), 0)  
    return (len(time_line), max(time_line)-min(time_line))


if __name__ == "__main__":
    community_gradiant = {}
    for commun in os.listdir(communities):
        path = communities+'/'+commun
        check = '/Users/miaaltieri/Research_Data/Comm_Graphs/'+commun+"_graph.pickle"
        csv_file = open(path,"rt")
        if not os.path.isfile(check):
            print(commun)
            print("no graph like this exists :( ")
            continue
        community_gradiant[commun] = snap_shot_csv(csv_file)
    
        
    # this massive loop, prints the first 100 communites with the highest amount
    # of different months 
    top_100_commun = []
    for key, value in itertools.islice(sorted(community_gradiant.items(), key=operator.itemgetter(1),  reverse=True), 100):
        print (key, value)
        top_100_commun.append(key)
        

    print(top_100_commun)
    with open(result_path,'wb') as out:
      pickle.dump(top_100_commun, out)
        
    print(least)

