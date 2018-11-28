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
g = sns.catplot(x="Owners", y="LP", hue="Graphlet Type", kind="bar", data=df, ci=95);
g.fig.set_size_inches(14,8)
g.fig.get_axes()[0].set_yscale('log')








titanic = sns.load_dataset("titanic")
sns.set(font_scale=1.5)
sns.catplot(x="sex", y="survived", hue="class", kind="bar", data=titanic, ci=95);
g.fig.set_size_inches(14,8)
g.fig.get_axes()[0].set_yscale('log')






