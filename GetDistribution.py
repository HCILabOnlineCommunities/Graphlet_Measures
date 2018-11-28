#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 17:08:57 2018

@author: miaaltieri
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 17:21:56 2018

@author: miaaltieri
"""

import pickle 

graphlet_types = ["four_paths","four_tailedtriangles","three_stars","four_chordalcycles","four_cliques","four_cycles"]
mapToDict = { "four_paths": {},
             "four_tailedtriangles": {},
             "three_stars": {},
             "four_chordalcycles": {},
             "four_cliques": {},
             "four_cycles": {}      
             }

#------------------------------------------------------------------------------
# returns average LP for a graphlet type in a given community 
#------------------------------------------------------------------------------
def gatherLPFromComm(comm):
    print(comm)
    for graphlet_type in graphlet_types:
        
        path = LP_base_result_path + commun+graphlet_type+"_LP"
        
        #Load in the graph object
        graph = None
        with open(path,"rb") as f_p:
            graph = pickle.load(f_p, encoding='latin1')
            
        
        for graphlet in graph[graphlet_type]:
            list_of_LPs = graph[graphlet_type][graphlet]['LP']
            for LP in list_of_LPs:
                if LP not in  mapToDict[graphlet_type]:
                     mapToDict[graphlet_type][LP] = 0
                mapToDict[graphlet_type][LP] +=1
                
                

#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
if __name__ == "__main__":
    #global compute_leader 
    basepath = '/Users/miaaltieri/Research_Data/'
    LP_base_result_path = basepath + 'Results/LP_Results/'
    top_commun_path = basepath+'/Results/top_100_commun'
    top_100_commun = None
    
    with open(top_commun_path,"rb") as f_p:
        top_100_commun = pickle.load(f_p)
    
    for i,commun in enumerate(top_100_commun):
        print(i)
        gatherLPFromComm(commun)
        
       
            
    #--------------------------------------------------------------------------
    # save and compute final results        
    for g in graphlet_types:
        result_path = LP_base_result_path + "Distribution/"+g
        LP_distributions = mapToDict[g]
        with open(result_path,'wb') as out:
            pickle.dump(LP_distributions,out)
        
        

            
