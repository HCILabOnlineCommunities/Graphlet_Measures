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

import csv
import sys

# takes first 30 words from text and returns them 
def first_30(text) -> str:
    segment = ""
    words = text.split()
    for i in range(0, 29):
        segment = segment + words[i] + " "
    segment = segment + words[29]
    return segment

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
        text = first_30(row[5])
        time_line[time] = time_line[time] + text
    return time_line

if __name__ == "__main__":
    #Expect first argument to sys.argv is a csv filename
    #This csv file is expected to have headers and a column
    #header named "text"
    csv_file = open(sys.argv[1],"rt")
    snap_shot(csv_file)

    