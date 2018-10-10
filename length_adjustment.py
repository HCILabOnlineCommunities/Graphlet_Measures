# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 11:45:46 2017
@author: Ryan Compton
"""

import nltk, string
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.util import ngrams
from collections import Counter
import numpy as np
from nltk.corpus import stopwords 

remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

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
        self.tri_counts = Counter()
        #Build the Statistical Language Model
        print("Building SLM")
        self.build_model()
        print("Build Complete")
        
    #Need to separate out all text by sentences and then do tri-gram counts
    def build_model(self):
        #Gather the sentences within the text
        sentences = sent_tokenize(self.all_text)
        #Iterate through the list of sentences
        for sentence in sentences:
            #Tokenize the words within the sentence
            tokens = word_tokenize(sentence)
            #Remove Puncutation, lower case word, and lemmatize the word
            words = [self.lemma.lemmatize(word.lower()) for word in tokens if word.isalpha()]
            #Find the trigrams within the sentence
            trigrams = ngrams(words,3)
            #Add the tri-grams to the count dictionary
            self.tri_counts += Counter(trigrams)   
        #Hold the total count of all tri-grams
        self.total = sum(self.tri_counts.values())   
 
    #Find the probability of a sentence
    def sentence_prob(self,sentence):
        sent_tokens = self.sentence_tokens(sentence)
        #Start with prob of 1.0 since all probs are multiplied since
        #this is assuming "and":  P(tri-grams) = P(tri-gram1) * P(tri-gram2) * ...
        prob = 1.0
        #Iterate through all trigrams
        for tri_gram in ngrams(sent_tokens,3):
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

# cleans the text to remove punctuation, stopwords, etc
def clean_text(text):
    text = text.translate(remove_punctuation_map).lower()
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    return filtered_sentence

# takes first 30 words from text and returns them 
def first_30(text) -> str:
    return (clean_text(text)[0:30])
    


if __name__ == "__main__":
    text = """Southern California friends! This Saturday, my collective Disorient
    will be one of the sound stages at LA Decompression 2018. For my friends who 
    aren't Burners, Decompression is this is the official "after party" for 
    Burning Man — we come together in cities all around the world to celebrate 
    Burning Man culture, music, art, and community. We're bringing out a premium 
    sound system with music curated by (birthday boy!)"""
    
    print(first_30(text))