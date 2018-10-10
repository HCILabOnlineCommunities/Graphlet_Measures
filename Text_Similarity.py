#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 18:48:33 2018
@author: miaaltieri
This script computes the similarity of two sets of text, computes both
Jaccard Similarity and Cosine Similarity 
"""

import sys
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from sklearn.metrics import jaccard_similarity_score

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


# cleans the text to remove punctuation, stopwords, etc
def clean_text(text):
    text = text.translate(remove_punctuation_map).lower()
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    while len(filtered_sentence) < 30:
        filtered_sentence.extend([""])
    return filtered_sentence

# then puts the text into an array
def jaccard_similarity(text1, text2):
    text1 = clean_text(text1)
    while len(text1) < 30:
        text1.extend([""])
    text2 = clean_text(text2)
    while len(text2) < 30:
        text2.extend([""])
    return jaccard_similarity_score(text1,text2)

if __name__ == "__main__":
    #Expect first & second argument to be text with no more than 30 words
    text_file_0 = open(sys.argv[1],"rt")
    text_file_1 = open(sys.argv[2],"rt")
    print(cosine_sim(text_file_0,text_file_1))
    jaccard_similarity(text_file_0, text_file_1)
    