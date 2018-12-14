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
import pickle
 
graphlet_types = ["four_paths","four_tailedtriangles","three_stars","four_chordalcycles","four_cliques","four_cycles"]

Sparse = ['four_paths', 'three_stars']
Middle = ['four_cycles', 'four_tailedtriangles']
Dense = ['four_chordalcycles', 'four_cliques']

basepath = '/Users/miaaltieri/Research_Data/'
data = ['density','g-type','owners', 'LP']

data_as_dict = {}
density_type = []
graph_type = []
leaders = []
LP_val = []

top_commun_path = basepath+'/Results/top_100_commun'
top_100_commun = None

with open(top_commun_path,"rb") as f_p:
    top_100_commun = pickle.load(f_p)


for g in graphlet_types:
    data_graphlet = ['density','g-type','owners', 'LP']
    graphlet_LP = {}
    graph_type_graphlet = []
    leaders_graphlet = []
    LP_val_graphlet = []
    
    for percent, commun in enumerate(top_100_commun):
        density = ""
        if g in Sparse:
            density = 'Sparse'
        elif g in Middle: 
            density = 'Middle'
        else:
            density = 'Dense'
            

        
        leader_graph_path = basepath + "Results/LP_Results/"+ commun + g + "_leader_LP"
        
        #Load in the graph object
        leader_graph = None
        with open(leader_graph_path,"rb") as f_p:
            leader_graph = pickle.load(f_p, encoding='latin1')
            
        for number_of_leaders in range (0,5):
            LP_avg = leader_graph[g][number_of_leaders]['avg']
            if LP_avg != 'no graph data found': 
                res_row = [density, g, number_of_leaders, LP_avg]
                data.append(res_row)
                density_type.append(density)
                graph_type.append(g)
                leaders.append(number_of_leaders)
                LP_val.append(LP_avg)
                
                data_graphlet.append(res_row)
                graph_type_graphlet.append(g)
                leaders_graphlet.append(number_of_leaders)
                LP_val_graphlet.append(LP_avg)
                
                
    graphlet_LP['g-type']=graph_type_graphlet
    graphlet_LP['owners']=leaders_graphlet
    graphlet_LP['LP']=LP_val_graphlet
    
    
    df = pd.DataFrame(graphlet_LP)
    
    

    sns.set(font_scale=1.5)
    diagram = sns.catplot(x='owners', y='LP', kind="bar", palette="ch:.25", data=df, height=5, aspect=2);
    diagram.set(ylim=(0,6))
    axes = diagram.axes.flatten()
# =============================================================================
#     axes[0].set_title(g)
# =============================================================================
    diagram.fig.set_size_inches(14,8)
    

                
                    
    print(percent,"%")

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
result_path = '/Users/miaaltieri/Research_Data/Results/LP_Results_1st/LPByDensity'

#Load in the graph object
with open(result_path,"rb") as f_p:
    data = pickle.load(f_p, encoding='latin1')


graph_as_chart = [['','Graphlet Type', 'LP', 'Owners']]
denisities = []
LP = []
owners = []


for density, values in data.items():
    for leader, lp_val in values.items():
        denisities.append(density)
        owners.append(leader)
        LP.append(lp_val)
    
results = {}
results['Graphlet Type'] = denisities
results['LP'] = LP
results['Owners'] = owners

df = pd.DataFrame(results)

sns.set(font_scale=1.5)
g = sns.catplot(x="Owners", y="LP", hue="Graphlet Type", kind="bar", data=df, ci=.95);
g.fig.set_size_inches(14,8)
g.fig.get_axes()[0].set_yscale('log')
"""






"""
titanic = sns.load_dataset("titanic")
sns.set(font_scale=1.5)
sns.catplot(x="sex", y="survived", hue="class", kind="bar", data=titanic, ci=.95);
g.fig.set_size_inches(14,8)
g.fig.get_axes()[0].set_yscale('log')
"""






