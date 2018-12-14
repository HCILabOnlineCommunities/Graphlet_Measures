#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 12:27:03 2018

@author: miaaltieri
"""
import seaborn as sns
import numpy as np
import pandas as pd
import pickle
from  matplotlib.ticker import PercentFormatter


graphlet_type = ["four_paths","four_tailedtriangles","three_stars","four_chordalcycles","four_cliques","four_cycles"]



graph_as_chart = [['','four_chordalcycles', 'Distribution']]
 
    
for g in graphlet_type:
    all_count = 0
    result_path = '/Users/miaaltieri/Research_Data/Results/LP_Results/Distribution/'+g

    #Load in the graph object
    with open(result_path,"rb") as f_p:
        LP = pickle.load(f_p, encoding='latin1')
    
    
    graph_as_chart = [['',g, 'LingProg of Leaders']]
    names = []
    values = []
    
    for LP, count in (LP).items():
        all_count += count
        graph_as_chart.append(['',LP,count])
        names.append(LP)
        values.append(count)
        
        
    results = {}
    results[g] = names
    results['Distribution'] = values
    
    df = pd.DataFrame(results)
    #sns.set(rc={'figure.figsize':(11.7,20000000000)})
    g = sns.catplot(x=g, y='Distribution', kind="bar", palette="ch:.25", data=df, height=5, aspect=2)
    for ax in g.axes.flat:
        ax.yaxis.set_major_formatter(PercentFormatter(all_count))
    g.set(ylim=(0,all_count/10))
    g.set(ylabel="Percent")

    
"""

names = []
values = []
for num_lead, LP in (LP_AVG_leader[g]).items():
    
for key in sorted(LP.items())
    graph_as_chart.append(['',key,LP[key]])
    names.append(num_lead)
    values.append(LP[key])
    print(num_lead, LP[key])

results = {}
results[g] = names
results['LingProg of Leaders'] = values

df = pd.DataFrame(results)
sns.catplot(x=g, y='Distribution of four chords', kind="bar", palette="ch:.25", data=df, height=5, aspect=2);
  
"""



"""
#Load in the graph object
with open(result_path,"rb") as f_p:
    LP_AVG_leader = pickle.load(f_p, encoding='latin1')
    
for g in graphlet_type:
    for num_lead, LP in (LP_AVG_leader[g]).items():
        print(num_lead, LP["avg"])
        
    graph_as_chart = [['',g, 'LingProg of Leaders']]
    names = []
    values = []
    for num_lead, LP in (LP_AVG_leader[g]).items():
        graph_as_chart.append(['',num_lead,LP["avg"]])
        names.append(num_lead)
        values.append(LP["avg"])
        print(num_lead, LP["avg"])
        
        
    results = {}
    results[g] = names
    results['LingProg of Leaders'] = values
    
    df = pd.DataFrame(results)
    #sns.set(rc={'figure.figsize':(11.7,20000000000)})
    sns.catplot(x=g, y='LingProg of Leaders', kind="bar", palette="ch:.25", data=df, height=5, aspect=2);
  """  

"""
#Load in the graph object
with open(result_path,"rb") as f_p:
    graphs = pickle.load(f_p, encoding='latin1')
    
graph_as_chart = [['','Name', 'LingProg']]
names = []
values = []
for graph_type,LP in graphs.items():
    graph_as_chart.append(['',graph_type,LP[2]])
    names.append(graph_type)
    values.append(LP[2])
    
results = {}
results['Name'] = names
results['Values'] = values

df = pd.DataFrame(results)
#sns.set(rc={'figure.figsize':(11.7,20000000000)})
sns.catplot(x="Name", y="Values", kind="bar", palette="ch:.25", data=df, height=5, aspect=2);
"""






    

#print (graph_as_chart)

#titanic = sns.load_dataset("titanic")

#sns.catplot(x="deck", kind="count", palette="ch:.25", data=titanic)






