# Author: Angela Ramirez
    #5/11/2018
# *****************************

import os
import pickle
import time


print("asdfadfadsf")
start = time.gmtime()
print (str(start[3])+":"+str(start[4])+":"+str(start[5]))

#comm is the first key
   #keys to retrieve info
        # reply_author
        # Comm_Ref_RA
        # Original_post_author
        # Comm_Ref_OA
        #reply_text
        #reply_title
        # reply_date
        # Original_post_text
        # Original_post_title
        # Original_date	tool

edge = None
with open('edge_feats.pickle', 'rb') as fp:    
    edge = pickle.load(fp, encoding='latin1')
    print (type(edge))


# look for main graphlet pickle
# tailed_triangles and cliques
# PATH FOR FILE
path = 'C:\\Users\\Mia\\Desktop\\School\\Research\\Subgraphs\\Graphlets_Easy_Access'

#open using pickle library (dictionary type)
with open(os.path.join(path, " .pickle"), "rb") as f_p:
    path = pickle.load(f_p, encoding='latin1')
    print (type(path))

#finding text
gather_text = []
#path - 1st layer: gets you the list(filled with dictionary) associated with type

path = path[0:len(path)/2]

for ty_list in path:
    #comm is the key with this dict
    for comm in ty_list:    
        if comm+"_replies.csv" in edge:
            #way to grab things from the dictionary
            og_author = [x['Comm_Ref_OA'] for x in edge[comm+"_replies.csv"]]
            og_post = [x['Original_post_text'] for x in edge[comm+"_replies.csv"]]
            og_reply = [x["reply_text"] for x in edge[comm+"_replies.csv"]]

            #once you get the communities you get into the list of graphlets
            for g in ty_list[comm]:
                #once you get the graphlet iterate through to get the user
                for user in g:
                    #i is of type string so does not work unless user is type string
                    if str(user) in og_author:
                        gather_text.append(og_post[og_author.index(str(user))])
        #                 print gather_text

#reference
    #pickle.dump()

end = time.gmtime()
print (str(end[3]) + ":" + str(end[4]) + ":" + str(end[5]))

path = 'C:\\Users\\Mia\\Desktop\\School\\Research\\Subgraphs\\Graphlets_Pure_Text'

with open(os.path.join(path, "Four_tailed_triangles_text.pickle"),'wb') as out:
    pickle.dump(gather_text,out)
