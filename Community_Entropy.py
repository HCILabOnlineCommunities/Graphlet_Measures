# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 11:45:46 2017
@author: Ryan Compton
"""

import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.util import ngrams
from collections import Counter
import numpy as np

import os
import datetime
import pickle
import string
from nltk.corpus import stopwords 

graphlet_type = ["four_paths","four_tailedtriangles","three_stars","four_chordalcycles","four_cliques","four_cycles"]
#graphlet_type = ["four_cliques"]
basepath = '/Users/miaaltieri/Research_Data/'
# "Results/top_100_commun"


# this is the structure for the dictionary that we repeatedly pickle at the end 
# graphlet_entropy = {}
# graphlet_entropy[Graphlet_Type] = {}
# graphlet_entropy[Graphlet_Type][Graphlet] = {}
# graphlet_entropy[Graphlet_Type][Graphlet]["entropy"]  = []
# graphlet_entropy[Graphlet_Type][Graphlet]["entropy_AVG"]  = number 

# Graphlet_Type is a string indicating one of the 6 graphlet types we are exploring 
# Graphlet provides the nodes that make up a graphlet
# "entropy" key pointing to the Linguistic Progressiveness measure for each post,
#     hence it returnong a list
# "entropy_AVG" key pointing to the average of the list "entropy"


# so this right here is a dictionary that will store the entropy of each post, the
# key is a unique key 
# since in our loop we look at original text, original title, we will use this 
# as a key along with the original author
# key = Original Post Date+"_"+Original Post Title+"_"+Original Author+commun
# value = entropy
posts_entropy = {}
# this is a string since entropy for a graph can be a double so its best to compare
# it with something it could never be, a string
NO_GRAPH_DATA = "no graph data found"
COSINE_FAIL = -1 


remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


#-----------------------------------------------------------------------------
#       Mia Counter
#-----------------------------------------------------------------------------
class Counter_mia:
    def __init__(self):
        self.counter = {}
        self.number_of_unique_items = 0
        
    def add(self, items):
        #print((list(items)))
        for elem in items:
            if elem not in self.counter:
                self.counter[elem]=0
                self.number_unique_of_items +=1
            self.counter[elem]+=1
            
            
    
    # count unique keys MIA TODO:
    def total_unique_number_of_items(self):
        return self.number_of_unique_items

    def get(self, first, second):
        return self.counter.get(first,second)
    
#-----------------------------------------------------------------------------
#       START SML CLASS
#-----------------------------------------------------------------------------
class SLM:
    #Inputs:
    #   text is a string holding the total amount of text from the sample
    #   tools is a list of tools to account for multiple text sources:
    #       Expected: "Wiki", "Blog", "Forum", "BlogCmt", "ForumRep"
    def __init__(self, text,tools=None,encoding="utf-8"):
        #Store the text provided
        self.all_text = text
        #Store the tool information for filtering which tool to use
        self.tools = tools
        #Set encoding to "utf-8" but allow for other encodings
        #Another one to expect is "latin-1"
        self.encoding = encoding
        #Initialize lemmatize model
        self.lemma = nltk.wordnet.WordNetLemmatizer()
        #Initialze total tri-gram counter dictionary
        self.tri_counts = Counter_mia()                                         #self.tri_counts = Counter()
        #Build the Statistical Language Model
       # print("Building SLM")
        self.build_model()
       # print("Build Complete")
        
    #Need to separate out all text by sentences and then do tri-gram counts
    def build_model(self):
        counting_trigrams = 0
        for post in self.all_text:
            #Gather the sentences within the text
            sentences = sent_tokenize(post)
            #Iterate through the list of sentences
            for sentence in sentences:
                #Tokenize the words within the sentence
                tokens = word_tokenize(sentence)
                #Remove Puncutation, lower case word, and lemmatize the word
                words = [self.lemma.lemmatize(word.lower()) for word in tokens if word.isalpha()]
                #Find the trigrams within the sentence
                if len(words) < 3:
                    continue
                trigrams = list(ngrams(words,3))
                #Add the tri-grams to the count dictionary
                self.tri_counts.add(trigrams)                                       #self.tri_counts += Counter(trigrams)   
            counting_trigrams += self.tri_counts.number_of_unique_items             #self.total = sum(self.tri_counts.values())   
        #Hold the total count of all tri-grams
        self.total = counting_trigrams
        
    #Find the probability of a sentence
    def sentence_prob(self,sentence):
        sent_tokens = self.sentence_tokens(sentence)
        #Start with prob of 1.0 since all probs are multiplied since
        #this is assuming "and":  P(tri-grams) = P(tri-gram1) * P(tri-gram2) * ...
        prob = 1.0
        #Iterate through all trigrams
        # RYAN WHAT SHOULD WE DO, RETURN 0, A LOW NUBER, OR A FLAG?
        if len(sent_tokens) < 3:
            return .00000000000000001
        for tri_gram in ngrams(sent_tokens,3):
            # RYAN SOMETIMES self.total is 0 what should we do in this case?
            if self.total == 0:
                return .00000000000000001
            prob *= (float(self.tri_counts.get(tri_gram,0))/self.total)
        return prob

    #Gather the tokens of a sentence
    def sentence_tokens(self,sentence):
        sent_tokens = [self.lemma.lemmatize(word.lower()) for word in word_tokenize(sentence) if word.isalpha()]
        return sent_tokens

    #Find the probability of text
    def text_prob(self,text):
        sentences = sent_tokenize(text)
        prob = 1.0
        for sentence in sentences:
            prob *= self.sentence_prob(sentence)
        return prob

    #Find the entropy of text
    def entropy(self,text):
        probs = []
        for sentence in sent_tokenize(text):
            sent_num_words = len([self.lemma.lemmatize(word.lower()) for word in word_tokenize(sentence) if word.isalpha()])
            sentence_prob = self.sentence_prob(sentence)
            if float(sent_num_words) == 0 or sentence_prob == 0:
                probs.append(1)
            else:
                probs.append(-1*np.log(sentence_prob) / float(sent_num_words))
        if len(probs) == 0:
            return 1
        avg_entropy = sum(probs) / float(len(probs))
        return avg_entropy

    #Find the prototypicality of text
    def prototypicality(self, text):
        #text = text.decode(self.encoding)
        entropy = self.entropy(text)
        prototypicality = -1*entropy
        return prototypicality

#-----------------------------------------------------------------------------
#       END SML CLASS
#-----------------------------------------------------------------------------

# cleans the text to remove punctuation, stopwords, etc
def clean_text(text):
    text = text.translate(remove_punctuation_map).lower()
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    return filtered_sentence[0:30]

# converts month into a number
def convert_month(month) -> int:
    months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
              "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
    
    return months[month]

# returns a dictionary of SLMs, one SLM for each month within the community
def snap_shot_graph(comm_graph) -> dict:
    time_line = {}    
    SML_months = {}
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
            space = ' '
            text = space.join(text)
            
            # if after cleaning there is no text remaining then skip
            if len(text) == 0:
                continue
            
            if time not in time_line:
                time_line[time] = []
                
            time_line[time].append(text)
            
    for month, posts in time_line.items():
        SML_months[month] = SLM(posts,encoding="latin-1")
        
    return SML_months

# expects that post_content and snap_shots and computes the prototypically
# of that post content to the k*2 months surrounding it 
def prototypically(k, post_content, post_time, snap_shots) -> int:
    prototypically_min = float("-inf")
    index_min = post_time
    for i in range (post_time-k, post_time+k+1):
        if i == post_time:
            continue
        
        if i not in snap_shots:
            continue
        
        SML_i = snap_shots[i]
        prototypically = SML_i.prototypicality(post_content)
        if prototypically < prototypically_min:
            prototypically_min = prototypically
            index_min = i
    
    return index_min-post_time

# returns a dictionary where the key is the subgraph and the value is its
# progressive rating
def progressiveness_wi_commun(k, snap_shots, comm_graph, graphlet_type, commun, graphlet_entropy):
    path_to_comm_graphlets = basepath+graphlet_type+"/"+commun+"_graph_graphlets.pickle"
    graphlets = None
    entropy_sum = 0
    #Load in the graphlets
    with open(path_to_comm_graphlets,"rb") as f_p:
        graphlets = pickle.load(f_p, encoding='latin1')
    
    graphlet_entropy[graphlet_type] = {}
    
    # go through the list of the graphlets
    for graphlet_count, graphlet in enumerate(graphlets):
        #Grab the subgraph
        subg = comm_graph.subgraph(graphlet)
        graphlet_entropy[graphlet_type][graphlet_count] = {} #subg.edges
        graphlet_entropy[graphlet_type][graphlet_count]["entropy"] = []
        sum_entropy = 0
        
        #Iterate through edges in subgraph
        for edge in subg.edges:
            #loop through each post_reply pair in the edge (i.e. looping through list_index)
            for post in comm_graph.edges[edge]["post_reply_data"]: 
                post_key = post["Original_Date"]+"_"+post["Original_Title"]+"_"+str(post["Orig_auth"])+commun
                if post_key not in posts_entropy:
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
                    posts_entropy[post_key] = prototypically(k, sentence, time, snap_shots)
                    
                graphlet_entropy[graphlet_type][graphlet_count]["entropy"].append(posts_entropy[post_key])
                sum_entropy += posts_entropy[post_key]
        
        graphlet_entropy[graphlet_type][graphlet_count]["entropy_AVG"]= sum_entropy/len(graphlet_entropy[graphlet_type][graphlet_count]["entropy"])
        entropy_sum = entropy_sum + graphlet_entropy[graphlet_type][graphlet_count]["entropy_AVG"]    
    
    if len(graphlets) == 0:
        return NO_GRAPH_DATA
    
    return entropy_sum/len(graphlets)

if __name__ == "__main__":
    entropy_AVG_graphlet = {}
    entropy_AVG_result_path = basepath + "Results/Entropy_Results/Entropy_AVG"
    top_commun_path = basepath+"/Results/top_100_commun"
    
    with open(top_commun_path,"rb") as f_p:
            top_100_commun = pickle.load(f_p)
    
    for commun in top_100_commun:
        print(datetime.datetime.now(),commun)
        comm_path = basepath + "Comm_Graphs/" + commun+"_graph.pickle"
        result_path = basepath + "Results/Entropy_Results/"+ commun + "_Entropy"
        graphlet_entropy = {}
        
#        if os.path.isfile(result_path):
#            continue
        
        #Load in the graph object
        with open(comm_path,"rb") as f_p:
            comm_graph = pickle.load(f_p, encoding='latin1')
        
        snap_shots = snap_shot_graph(comm_graph)
        for g in graphlet_type:
            graphlet_entropy[g] = {}
            entropy = progressiveness_wi_commun(12, snap_shots, comm_graph, g, commun, graphlet_entropy)
            if g not in entropy_AVG_graphlet:
                entropy_AVG_graphlet[g] = [0,0,0]
            
            if entropy != NO_GRAPH_DATA:
                entropy_AVG_graphlet[g][0] += 1 
                entropy_AVG_graphlet[g][1] += entropy
    
        with open(result_path,'wb') as out:
            pickle.dump(graphlet_entropy,out)
            
    for g in graphlet_type:
        entropy_AVG_graphlet[g][2] = entropy_AVG_graphlet[g][1]/entropy_AVG_graphlet[g][0]
        print(entropy_AVG_graphlet[g][1],entropy_AVG_graphlet[g][0],entropy_AVG_graphlet[g][2])
        
    with open(entropy_AVG_result_path,'wb') as out:
        pickle.dump(entropy_AVG_graphlet,out)
          
    

