import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")


relationA=['act action add addition','attend attention decide decision','die death feed food', 'see scene grow growth','move movement advise advice','choose choice challenge challenge']
relationB=['buy bought eat ate','become became begin began','accept accepted add added','think thought build built','break broke wake woke','win won see saw','hold held hurt hurt','keep kept know knew','find found give gave','say said happen happened','offer offered open opened','pass passed tell told']

def nbest(relation):
    best1=0
    best5=0
    best10=0
    for r in relation:
        wordlist=r.split(' ')

        w1 = word_to_vec_dict[wordlist[0]]
        w2 = word_to_vec_dict[wordlist[1]]
        w4 = word_to_vec_dict[wordlist[3]]
        ret = distsim.show_nearest(word_to_vec_dict,
                                   w1-w2+w4,
                                   set([wordlist[0],wordlist[1],wordlist[3]]),
                                   distsim.cossim_dense)
        print ret
        if wordlist[2] == ret[0][0]:
            best1 += 1
        for r in range(5):
            if wordlist[2] == ret[r][0]:
                best5 += 1
        for r in range(10):
            if wordlist[2] == ret[r][0]:
                best10 += 1
    totalword = len(relation)
    accbest1 = round(float(best1) / totalword, 2)
    accbest5 = round(float(best5) / totalword, 2)
    accbest10 = round(float(best10) / totalword, 2)
    return accbest1,accbest5,accbest10

print nbest(relationA)
print nbest(relationB)
