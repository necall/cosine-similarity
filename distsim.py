from __future__ import division
import sys,json,math
import os
import numpy as np
import math

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict

def cossim_sparse(v1,v2):
    # Take two context-count dictionaries as input
    # and return the cosine similarity between the two vectors.
    # Should return a number beween 0 and 1
    uptotal=0
    for key in v1:
        if key in v2:
            uptotal+=v1[key]*v2[key]

    preproduct=0; nextproduct=0
    for i in v1:
        preproduct+=math.pow(v1[i],2)
    predown=math.sqrt(preproduct)

    for j in v2:
        nextproduct+=math.pow(v2[j],2)
    nextdown=math.sqrt(nextproduct)

    downtotal=predown*nextdown

    return float(uptotal)/float(downtotal)

def cossim_dense(v1,v2):
    # v1 and v2 are numpy arrays
    # Compute the cosine simlarity between them.
    # Should return a number between -1 and 1
    V1=np.array(v1)
    V2=np.array(v2)
    uptotal=0
    for v in V1*V2:
        uptotal+=v
    downf=0
    for v11 in np.power(V1,2):
        downf+=v11
    downfront=math.sqrt(downf)
    downb=0
    for v22 in np.power(V2,2):
        downb+=v22
    downback=math.sqrt(downb)
    return uptotal/(downfront*downback)

def show_nearest(word_2_vec, w_vec, exclude_w, sim_metric):
    #word_2_vec: a dictionary of word-context vectors. The vector could be a sparse (dictionary) or dense (numpy array).
    #w_vec: the context vector of a particular query word `w`. It could be a sparse vector (dictionary) or dense vector (numpy array).
    #exclude_w: the words you want to exclude in the responses. It is a set in python.
    #sim_metric: the similarity metric you want to use. It is a python function
    # which takes two word vectors as arguments.

    # return: an iterable (e.g. a list) of up to 10 tuples of the form (word, score) where the nth tuple indicates the nth most similar word to the input word and the similarity score of that word and the input word
    # if fewer than 10 words are available the function should return a shorter iterable
    #
    # example:
    #[(cat, 0.827517295965), (university, -0.190753135501)]

    simdic={}
    for word in word_2_vec:
        if word not in exclude_w:
            point=sim_metric(word_2_vec[word],w_vec)
            simdic[word]=point
    simdict=sorted(simdic.iteritems(),key=lambda d:d[1], reverse=True)
    # if len(simdict)<11:
    #     return simdict
    # else:
    return simdict[:10]
