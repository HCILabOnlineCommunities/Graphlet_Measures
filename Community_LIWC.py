#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 14:47:41 2018

@author: miaaltieri
"""



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 18:42:41 2018

@author: miaaltieri

Given a community, this python script will calculate the Linguistic Progressiveness
of a graphlet within respect to this community


This script is meant to be run multiple times,
i.e.  for f in *; do python Community_Ling_Prog.py f; done
"""
import os, sys
import datetime
import pickle
import nltk, string
import unicodedata
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from gather_features_LIWC_Sub_Emo_POS import score_text, default_dictionary_filename, load_dictionary


"""
LIWC_graphlet_results: graphlet_type : LIWC_cat : list of values

LIWC_graphlet_results {
        'three-star': {
            'First Person Pronoun' : [1,4,2,...]
            ...
        }
        ...
}
    
LIWC_leader_results : graphlet_type : number_of_leaders : LIWC_cat : list of values

LIWC_leader_results {
        'three-star': {
            0: {
                    'First Person Pronoun' : [1,4,2,...]
                    ...
            }
            ...
        }
        ...
}
"""

posts_LIWC = {}
LIWC_cats = ['Inclusive','Achievement','First Person Singular','Exclusive','First Person Plural', 'Anger','Anxiety','Work','Leisure','Inhibition','Assent','Articles']
graphlet_type = ["four_paths","four_tailedtriangles","three_stars","four_chordalcycles","four_cliques","four_cycles"]
compute_leader = 0


remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

#------------------------------------------------------------------------------
# cleans the text to remove punctuation, stopwords, etc
#------------------------------------------------------------------------------
def clean_text(text):
    text = unicodedata.normalize("NFKD",text)
    text = text.replace("â","")
    text = text.replace("Â","")
    text = text.translate(remove_punctuation_map).lower()
    return text.split()

#------------------------------------------------------------------------------
# returns a dictionary of LIWC categories & values
#------------------------------------------------------------------------------
def score_LIWC(text):
    scores = {}
    all_scores = score_text(text)
    for cat in LIWC_cats:
        scores[cat]=all_scores[cat]
    return scores

#------------------------------------------------------------------------------
# fills posts_LIWC and posts_leaders_LIWC
#------------------------------------------------------------------------------
def LIWC_wi_commun(comm_graph, graphlet_type, commun, LIWC_leader_results, LIWC_graphlet_results):
    #--------------------------------------------------------------------------
    # inital set up
    path_to_comm_graphlets = basepath+graphlet_type+"/"+commun+"_graph_graphlets.pickle"
    graphlets = None
    LIWC_results = {}
    count_LIWC = 0
    #Load in the graphlets
    with open(path_to_comm_graphlets,"rb") as f_p:
        graphlets = pickle.load(f_p, encoding='latin1')
       
    #--------------------------------------------------------------------------
    # go through the list of the graphlets and compute LP
    for graphlet_count, graphlet in enumerate(graphlets):
        #Grab the subgraph
        subg = comm_graph.subgraph(graphlet)
        
        # count leaders 
        number_of_leaders = 0
        for user in graphlet:
            if (comm_graph.nodes[user])['role'] == 'owner':
                number_of_leaders += 1
            
        #Iterate through edges in subgraph
        for edge in subg.edges:
            #loop through each post_reply pair in the edge (i.e. looping through list_index)
            for post in comm_graph.edges[edge]["post_reply_data"]: 
                post_key = post["Original_Date"]+"_"+post["Original_Title"]+"_"+str(post["Orig_auth"])+commun
                if post_key not in posts_LIWC:
                    if post["Tool"] == 'Wiki' or post["Tool"] == 'Idea' or post["Tool"] == 'IdeaCmt':
                        continue
                    
                    date = post["Reply_Date"].split()
                    if int(date[5]) <  2006:
                        continue
                    
                    text = post["Original_Text"]

                    text = text.replace(post["Original_Title"],"")
                    text = clean_text(text)
                    space = ' '
                    sentence = space.join(text)
                    posts_LIWC[post_key] = score_LIWC(sentence)
                    
                count_LIWC += 1
                LIWC_results_post = posts_LIWC[post_key]
                for cat,val in LIWC_results_post.items():
                    if cat not in LIWC_results:
                        LIWC_results[cat] = 0
                    LIWC_results[cat] += val
                    
            
    for cat,val in LIWC_results.items():
        LIWC_graphlet_results[graphlet_type][cat]['avg'] = val/count_LIWC
        LIWC_leader_results[graphlet_type][number_of_leaders][cat]['avg'] = val/count_LIWC
            
#------------------------------------------------------------------------------
# inital setup of dictionaries LIWC, LIWC_graphlet_results &
# LIWC_leader_results
#------------------------------------------------------------------------------
def Setup_Dicts ():
    dictionary_filename = default_dictionary_filename()
    load_dictionary(dictionary_filename)
    
    for g_type in graphlet_type:
        LIWC_graphlet_results[g_type]={}
        LIWC_leader_results[g_type]={}
        for leaders in range(0,5):
            LIWC_leader_results[g_type][leaders]={}
            for cat in LIWC_cats:
                LIWC_leader_results[g_type][leaders][cat]={}
                
        for cat in LIWC_cats:
            LIWC_graphlet_results[g_type][cat]={}         
            

        

#------------------------------------------------------------------------------
# main method
#------------------------------------------------------------------------------
if __name__ == "__main__":
    basepath = '/Users/miaaltieri/Research_Data/'
    top_commun_path = basepath+"/Results/top_100_commun"
    

    #If first arg is Leaders then compute leaders as well :)
    leader = sys.argv[1]
    if leader == "leaders":
        print("computing leaders as well")
        compute_leader = 1
    
    with open(top_commun_path,"rb") as f_p:
            top_100_commun = pickle.load(f_p)
     
    for num, commun in enumerate(top_100_commun):
        print(datetime.datetime.now(),commun)

        LIWC_graphlet_results = {}
        LIWC_leader_results = {}
        
        Setup_Dicts()
        
        comm_path = basepath + "Comm_Graphs/" + commun+"_graph.pickle"
        LIWC_result_path = basepath + "Results/LIWC_Results/General/"+commun
        LIWC_leader_result_path = basepath + "Results/LIWC_Results/ByLeader/"+commun

        #Load in the commun graph object
        with open(comm_path,"rb") as f_p:
            comm_graph = pickle.load(f_p, encoding='latin1')

        for g in graphlet_type:
           LIWC_wi_commun(comm_graph, g, commun, LIWC_leader_results, LIWC_graphlet_results)
           
        print(num,"% done")
    

    
        # save and final results        
        with open(LIWC_result_path,'wb') as out:
            pickle.dump(LIWC_graphlet_results, out)
            
        with open(LIWC_leader_result_path,'wb') as out:
            pickle.dump(LIWC_leader_results,out)


          
    
    