#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 12:15:28 2018

@author: miaaltieri


-Rebuild LP visual for each graphlet as one bar plot. This would have the
X-axis being the number of Owners, the Y-axis being the LP, and the bars being 
the different groups of densities in graphlets (or the Hue parameter within 
seaborn). Here is the density categorization:

Sparse: Four-Path, Three-Star
Middle: Four-Cycle, Four-TailedTriangle
Dense: Four-Chordalcycle, Four-Clique
"""
import pickle

graphlet_type = ["four_paths","four_tailedtriangles","three_stars","four_chordalcycles","four_cliques","four_cycles"]

Sparse = ['four_paths', 'three_stars']
Middle = ['four_cycles', 'four_tailedtriangles']
Dense = ['four_chordalcycles', 'four_cliques']

All = {'Sparse': {0:0, 1:0, 2:0, 3:0, 4:0},
       'Middle': {0:0, 1:0, 2:0, 3:0, 4:0},
       'Dense': {0:0, 1:0, 2:0, 3:0, 4:0}
      }


result_path = '/Users/miaaltieri/Research_Data/Results/LP_Results_1st/LP_AVG_Leader'

with open(result_path,"rb") as f_p:
    LP_AVG_leader = pickle.load(f_p, encoding='latin1')
    
# put values into dictionary All
for g in graphlet_type:
    key = ""
    if g in Sparse:
        key = 'Sparse'
    elif g in Middle: 
        key = 'Middle'
    else:
        key = 'Dense'
    
    for num_lead, LP in (LP_AVG_leader[g]).items():
        All[key][num_lead] = All[key][num_lead] + LP['avg']
        
# find average 
for key in All:
    for num_lead in range(0,5):
         All[key][num_lead] = All[key][num_lead]/2
         print(key, All[key][num_lead])
      
print("\n\n\n",All,"\n\n\n")
        
result_output_path = '/Users/miaaltieri/Research_Data/Results/LP_Results_1st/LPByDensity'      
with open(result_output_path,'wb') as out:
    pickle.dump(All,out)
        

