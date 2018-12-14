#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 08:21:46 2018

@author: miaaltieri
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 12:21:06 2018

@author: miaaltieri
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 12:27:03 2018

@author: miaaltieri
"""
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
import pickle
 
graphlet_types = ["four_paths","four_tailedtriangles","three_stars","four_chordalcycles","four_cliques","four_cycles"]

Sparse = ['four_paths', 'three_stars']
Middle = ['four_cycles', 'four_tailedtriangles']
Dense = ['four_chordalcycles', 'four_cliques']

basepath = '/Users/miaaltieri/Research_Data/'
data = ['density','g-type','owners', 'LP']
LIWC_cats = ['Inclusive','Exclusive','First Person Plural','First Person Singular']


data_as_dict = {}
density_type = []
graph_type = []
leaders = []
LP_val = []

missing_data = 0
contains_data = 0

top_commun_path = basepath+'/Results/top_100_commun'
top_100_commun = None

with open(top_commun_path,"rb") as f_p:
    top_100_commun = pickle.load(f_p)

graphlet_LIWC = {}

#       B: comment this in to 
graphlet_LIWC['difference value'] = []
graphlet_LIWC['type'] = []      

"""
graphlet_LIWC['LIWC cat'] = []
graphlet_LIWC['LIWC val'] = []    
graphlet_LIWC['Density'] = [] 
"""

for number_of_leaders in range (0,5):

    
    for g in graphlet_types:
        data_graphlet = ['density','g-type','owners', 'LP']
        
        
        #       A: comment this in to get all of the LIWC ratings for a
        #          graphlet type

        

        
        for percent, commun in enumerate(top_100_commun):
            """
            density = ""
            if g in Sparse:
                density = 'Sparse'
            elif g in Middle: 
                density = 'Middle'
            else:
                density = 'Dense'
                
            if density != 'Dense':
                continue
            """
              
            #Load in the graph object
            leader_graph_path = basepath + "Results/LIWC_Results/ByLeader/"+ commun 
            LIWC_leader_results = None
            with open(leader_graph_path,"rb") as f_p:
                LIWC_leader_results = pickle.load(f_p, encoding='latin1')
                
            
            inclusive_sum = 0
            exclusive_sum = 0
            plural_sum = 0
            singular_sum = 0
            for cat in LIWC_cats:
                if LIWC_leader_results[g][number_of_leaders][cat] == {}:
                    missing_data +=1
                    continue
                else:
                    contains_data +=1
                
                LIWC_avg = LIWC_leader_results[g][number_of_leaders][cat]['avg']
                
                """
                #       A: comment this in to get all of the LIWC ratings for a
                #          graphlet type
                graphlet_LIWC['LIWC cat'].append(cat)
                graphlet_LIWC['LIWC val'].append(LIWC_avg)
                graphlet_LIWC['Density'].append(density)
                """
                
                #       B: comment this in to get plur sing incl excl for each
                #          graphlet type
                if (cat == 'Inclusive'):
                    inclusive_sum += LIWC_avg
                if (cat == 'Exclusive'):
                    exclusive_sum += LIWC_avg
                if (cat == 'First Person Plural'):
                    plural_sum += LIWC_avg
                if (cat == 'First Person Singular'):
                    singular_sum += LIWC_avg
                
                """
            diff_inc_exc_divisor = (inclusive_sum + exclusive_sum)/2
            diff_plur_sing_divisor = (plural_sum + singular_sum)/2
            
            diff_inc_exc = 0
            if diff_inc_exc_divisor != 0:
                diff_inc_exc = (inclusive_sum - exclusive_sum)/diff_inc_exc_divisor
            
            diff_plur_sing = 0
            if diff_plur_sing_divisor != 0:
                diff_plur_sing = (plural_sum - singular_sum)/diff_plur_sing_divisor
                """
            diff_inc_exc = (inclusive_sum - exclusive_sum)
            diff_plur_sing = (plural_sum - singular_sum) 
            
            
            graphlet_LIWC['difference value'].append(diff_inc_exc)
            graphlet_LIWC['type'].append('Incl-Excl')
            graphlet_LIWC['difference value'].append(diff_plur_sing)
            graphlet_LIWC['type'].append('Plur-Sing')
        

    #       B: comment this in to get plur sing incl excl for each
    #          graphlet type              
    df = pd.DataFrame(graphlet_LIWC)
    sns.set(font_scale=.9)
    diagram = sns.catplot(x='type', y='difference value', kind="bar", palette="ch:.25", data=df, height=5, aspect=2);
    diagram.set(ylim=(-.3,2))
    axes = diagram.axes.flatten()
    title = str(number_of_leaders)+" leaders"
    axes[0].set_title(title)
    diagram.fig.set_size_inches(5,5)    

"""
B 
1. density is x y- freq of LIWC
achivement,
work,
articles, 
"""   
      

    
"""
#       A: comment this in to get all of the LIWC ratings for a
#          graphlet type
df = pd.DataFrame(graphlet_LIWC)
sns.set(font_scale=.9)
diagram = sns.catplot(x='LIWC cat', y='LIWC val', kind="bar", palette="ch:.25", data=df, height=5, aspect=2);
#diagram.set(ylim=(0,10))
diagram.fig.get_axes()[0].set_yscale('log')
# axes = diagram.axes.flatten()
diagram.fig.axes[0].set_title("Dense LIWC")
diagram.fig.set_size_inches(6,6)
"""


"""

print(missing_data,contains_data)

data_as_dict['density']=density_type
data_as_dict['g-type']=graph_type
data_as_dict['owners']=leaders
data_as_dict['LP']=LP_val
    
df = pd.DataFrame(data_as_dict)

sns.set(font_scale=1.5)
g = sns.catplot(x="owners", y="LP", hue="density", kind="bar", data=df, ci=.95);
g.fig.set_size_inches(14,8)
#g.fig.get_axes()[0].set_yscale('log')


leader_graph_path = basepath + "Results/LP_Results/All_LPs"
with open(leader_graph_path,'wb') as out:
    pickle.dump(data_as_dict,out)

 

"""




