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
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

# this is the structure for the dictionary that we repeatedly pickle at the end 
# graphlet_lp = {}
# graphlet_lp[Graphlet_Type] = {}
# graphlet_lp[Graphlet_Type][Graphlet] = {}
# graphlet_lp[Graphlet_Type][Graphlet]["LP"]  = []
# graphlet_lp[Graphlet_Type][Graphlet]["LP_AVG"]  = number 

# Graphlet_Type is a string indicating one of the 6 graphlet types we are exploring 
# Graphlet provides the nodes that make up a graphlet
# "LP" key pointing to the Linguistic Progressiveness measure for each post,
#     hence it returnong a list
# "LP_AVG" key pointing to the average of the list "LP"


# so this right here is a dictionary that will store the LP of each post, the
# key is a unique key 
# since in our loop we look at original text, original title, we will use this 
# as a key along with the original author
# key = Original Post Date+"_"+Original Post Title+"_"+Original Author+commun
# value = LP
posts_lp = {}

# this is a string since LP for a graph can be a double so its best to compare
# it with something it could never be, a string
NO_GRAPH_DATA = "no graph data found"
COSINE_FAIL = -1 
graphlet_type = ["four_paths","four_tailedtriangles","three_stars","four_chordalcycles","four_cliques","four_cycles"]
compute_leader = 0
basepath = '/Users/miaaltieri/Research_Data/'



remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
stemmer = nltk.stem.porter.PorterStemmer()
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

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    try:
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0,1]
    except:
        print("cosine sim fails")
        return COSINE_FAIL

# excpets that post_content and snap_shots
def ling_prog (k, post_content, post_time, snap_shots) -> int:
    entropy_min = -1
    index_min = post_time
    for i in range (post_time-k, post_time+k+1):
        if i == post_time:
            continue
        if i not in snap_shots:
            continue
        snapshot_i = snap_shots[i]
        entropy = cosine_sim(" ".join(snapshot_i), " ".join(post_content))
        if entropy == COSINE_FAIL:
            continue
        if entropy > entropy_min:
            entropy_min = entropy
            index_min = i
    
    if (abs(index_min-post_time) > 12 ):
        print("ERROR",index_min, post_time)
    return index_min-post_time

def snap_shot_graph(comm_graph) -> dict:
    time_line = {}    

    #loop through each edge in graph (i.e looping through edges)
    for edge in comm_graph.edges:
        #loop through each  post_reply pair in the edge (i.e. looping through list_index)
        for post in comm_graph.edges[edge]["post_reply_data"]: 
            if post["Tool"] == 'Wiki' or post["Tool"] == 'Idea' or post["Tool"] == 'IdeaCmt':
                continue           
            date = post["Reply_Date"].split()
            if int(date[5]) <  2006:
                continue
            
            text = post["Original_Text"] 
            time = (int(date[5])%2006)*12 + convert_month(date[1])
            text = text.replace(post["Original_Title"],"");
            text = clean_text(text)
            
            # if after cleaning there is no text remaining then skip
            if len(text) == 0:
                continue
            
            if time in time_line:
                time_line[time] = time_line[time] + text
            else:
                time_line[time] = text
            
    return time_line

#------------------------------------------------------------------------------
# returns average LP for a graphlet type in a given community 
#------------------------------------------------------------------------------
def progressiveness_wi_commun(k, snap_shots, comm_graph, graphlet_type, 
                              commun):
    #--------------------------------------------------------------------------
    # inital set up
    path_to_comm_graphlets = basepath+graphlet_type+"/"+commun+"_graph_graphlets.pickle"
    graphlet_lp = {}
    graphlet_leader_lp = {}
    
    graphlets = None
    LP_sum = 0
    
    #Load in the graphlets
    with open(path_to_comm_graphlets,"rb") as f_p:
        graphlets = pickle.load(f_p, encoding='latin1')

    graphlet_lp[graphlet_type] = {}
    
    # set up graphlet_leader_dict
    if compute_leader == 1:
        graphlet_leader_lp[graphlet_type] = {}
        for potential_leaders in range(0,5):
            graphlet_leader_lp[graphlet_type][potential_leaders] = {}
            graphlet_leader_lp[graphlet_type][potential_leaders]['sum'] = 0.0
            graphlet_leader_lp[graphlet_type][potential_leaders]['count'] = 0
            graphlet_leader_lp[graphlet_type][potential_leaders]['avg'] = 0.0
    
    
    #--------------------------------------------------------------------------
    # go through the list of the graphlets and compute LP
    for graphlet_count, graphlet in enumerate(graphlets):
        #Grab the subgraph
        subg = comm_graph.subgraph(graphlet)
        graphlet_lp[graphlet_type][graphlet_count] = {} 
        graphlet_lp[graphlet_type][graphlet_count]["LP"] = []
        sum_LP = 0
        count_LP = 0
        
        
        number_of_leaders = 0
        for user in graphlet:
            if (comm_graph.nodes[user])['role'] == 'owner':
                number_of_leaders += 1
            
        

        #Iterate through edges in subgraph
        for edge in subg.edges:
            #loop through each post_reply pair in the edge (i.e. looping through list_index)
            for post in comm_graph.edges[edge]["post_reply_data"]: 
                post_key = post["Original_Date"]+"_"+post["Original_Title"]+"_"+str(post["Orig_auth"])+commun
                if post_key not in posts_lp:
                    if post["Tool"] == 'Wiki' or post["Tool"] == 'Idea' or post["Tool"] == 'IdeaCmt':
                        continue
                    
                    date = post["Reply_Date"].split()
                    if int(date[5]) <  2006:
                        continue
                    
                    text = post["Original_Text"]
                    time = (int(date[5])%2009)*12 + convert_month(date[1])
                    text = text.replace(post["Original_Title"],"")
                    text = clean_text(text)
                    space = ' '
                    sentence = space.join(text)
                    posts_lp[post_key] = ling_prog(k, sentence, time, snap_shots)
                    
                graphlet_lp[graphlet_type][graphlet_count]["LP"].append(posts_lp[post_key])
                sum_LP += posts_lp[post_key]
                count_LP +=1
                
                # break on the first iteration
                break
        
            # break on the first iteration
            break
        
        
        graphlet_lp[graphlet_type][graphlet_count]["LP_AVG"]= sum_LP/count_LP
        LP_sum = LP_sum + graphlet_lp[graphlet_type][graphlet_count]["LP_AVG"]   
        
        if compute_leader == 1:
            graphlet_leader_lp[graphlet_type][number_of_leaders]['sum'] += sum_LP
            graphlet_leader_lp[graphlet_type][number_of_leaders]['count'] += count_LP
        
    
    #--------------------------------------------------------------------------
    # calculate values we will return and pickle necessary files
    result_path = basepath + "Results/LP_Results_1st/"+ commun + graphlet_type + "_LP"
    result_path_leader = basepath + "Results/LP_Results_1st/"+ commun + graphlet_type + "_leader_LP"
    leader_based_LP = None
    
    
    if compute_leader == 1:
        leader_based_LP = [None]*5
        for potential_leaders in range (0,5):
            lp_sum = graphlet_leader_lp[graphlet_type][potential_leaders]['sum']
            lp_count = graphlet_leader_lp[graphlet_type][potential_leaders]['count']

            if lp_count != 0:
                lp_leader_community_avg = lp_sum/lp_count
                graphlet_leader_lp[graphlet_type][potential_leaders]['avg'] = lp_leader_community_avg
                leader_based_LP[potential_leaders] = lp_leader_community_avg
            else:
                graphlet_leader_lp[graphlet_type][potential_leaders]['avg'] = NO_GRAPH_DATA
                leader_based_LP[potential_leaders] = NO_GRAPH_DATA
                
        with open(result_path_leader,'wb') as out:
            pickle.dump(graphlet_leader_lp, out)

    
    with open(result_path,'wb') as out:
        pickle.dump(graphlet_lp,out)
        
    regular_LP = NO_GRAPH_DATA
    if len(graphlets) != 0:  
        regular_LP = LP_sum/len(graphlets)
   
    return (regular_LP, leader_based_LP)





#------------------------------------------------------------------------------
#       main method
#------------------------------------------------------------------------------
if __name__ == "__main__":
    #global compute_leader 
    LP_AVG_graphlet = {}
    LP_AVG_leader = {}  
    LP_AVG_result_path = basepath + "Results/LP_Results_1st/LP_AVG"
    LP_AVG_leader_result_path = basepath + "Results/LP_Results_1st/LP_AVG_Leader"
    top_commun_path = basepath+"/Results/top_100_commun"
    
    #If first arg is Leaders then compute leaders as well :)
    leader = sys.argv[1]
    if leader == "leaders":
        print("computing leaders as well")
        compute_leader = 1
    
    with open(top_commun_path,"rb") as f_p:
            top_100_commun = pickle.load(f_p)
    
    for commun in top_100_commun:
        print(datetime.datetime.now(),commun)
        comm_path = basepath + "Comm_Graphs/" + commun+"_graph.pickle"
        result_path = basepath + "Results/LP_Results_1st/"+ commun + "_LP"

        
#        if os.path.isfile(result_path):
#            continue
        
        #Load in the graph object
        with open(comm_path,"rb") as f_p:
            comm_graph = pickle.load(f_p, encoding='latin1')
        
        snap_shots = snap_shot_graph(comm_graph)
        for g in graphlet_type:
            
            LP = progressiveness_wi_commun(12, snap_shots, comm_graph, g, commun)
            if g not in LP_AVG_graphlet:
                LP_AVG_graphlet[g] = [0,0,0]
            
            if LP[0] != NO_GRAPH_DATA:
                LP_AVG_graphlet[g][0] += 1 
                LP_AVG_graphlet[g][1] += LP[0]
                
            # here we want to add the values we found from that function and add it to our specific graph
            if compute_leader == 1:
                if g not in LP_AVG_leader:
                    LP_AVG_leader[g] = {}
                    for number_of_leaders in range (0,5):
                        LP_AVG_leader[g][number_of_leaders] = {'count':0,'sum':0,'avg':0}
                
                
                for number_of_leaders in range (0,5):
                    if LP[1] != NO_GRAPH_DATA and LP[1][number_of_leaders] != NO_GRAPH_DATA:
                        LP_AVG_leader[g][number_of_leaders]['count'] +=1
                        LP_AVG_leader[g][number_of_leaders]['sum'] += LP[1][number_of_leaders]
                        
        print("leader info calculated thus far")
        for g in graphlet_type:
            print(g,": ")
            for number_of_leaders in range (0,5):
                print (LP_AVG_leader[g][number_of_leaders]['count'], LP_AVG_leader[g][number_of_leaders]['sum'])
           
            
    #--------------------------------------------------------------------------
    # save and compute final results        
    for g in graphlet_type:
        LP_AVG_graphlet[g][2] = LP_AVG_graphlet[g][1]/LP_AVG_graphlet[g][0]
        print(LP_AVG_graphlet[g][1],LP_AVG_graphlet[g][0],LP_AVG_graphlet[g][2])
        
    with open(LP_AVG_result_path,'wb') as out:
        pickle.dump(LP_AVG_graphlet,out)
            
    if compute_leader == 1:
        for g in graphlet_type:
            for number_of_leaders in range (0,5):
                count = LP_AVG_leader[g][number_of_leaders]['count']
                if (count != 0):
                    sum_of_LP = LP_AVG_leader[g][number_of_leaders]['sum']
                    LP_AVG_leader[g][number_of_leaders]['avg'] = sum_of_LP/count
                    print(sum_of_LP, count, sum_of_LP/count)
        
    with open(LP_AVG_leader_result_path,'wb') as out:
        pickle.dump(LP_AVG_leader,out)

          
    
    