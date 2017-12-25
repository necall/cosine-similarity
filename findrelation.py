import distsim

def vailddigit(num):
    mark=0
    value=''
    strnum=str(num)
    for s in range(len(strnum)):
        if mark==1 and strnum[s]=='0':
            mark+=1
            if strnum[s+1]>=5:
                value+='1'
            else:
                value+='0'
            return value
        else:
            value+=strnum[s]
        if strnum[s]!='0'and strnum[s]!='.':
            mark+=1
        if mark==2:
            if len(strnum) == 4:
                return value
            elif strnum[s+1]>='5':
                a=str(int(value[-1])+1)
                # value[-1]=str(a+1)
                return value[:-1]+a
            return value
    return value
f1=open("word-test.v3.txt")
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")

fstring=''
for i in f1:
    fstring+=i
flist=fstring.split(':')
flist.remove(flist[0])

for f in flist:
    feachline=f.strip(' ').strip('').split('\n')
    for f in feachline:
        if f=='':
            feachline.remove(f)
    # print feachline
    best1=0
    best5=0
    best10=0
    title=''
    for ff in feachline:
        wlist=ff.strip(' ').strip('\t').split(' ')
        if len(wlist)==1:
            title=wlist
            continue

        w1=word_to_vec_dict[wlist[0].strip('\t')]
        w2=word_to_vec_dict[wlist[1].strip('\t')]
        w4=word_to_vec_dict[wlist[3].strip('\t')]
        ret = distsim.show_nearest(word_to_vec_dict,
                                   w1 - w2 + w4,
                                   set([wlist[0], wlist[1], wlist[3]]),
                                   distsim.cossim_dense)
        # print ret
        if wlist[2] == ret[0][0]:
            best1+=1
        for r in range(5):
            if wlist[2]==ret[r][0]:
                best5+=1
        for r in range(10):
            if wlist[2]==ret[r][0]:
                best10+=1
    totalword=len(feachline)-1
    accbest1=vailddigit(float(best1) / totalword)
    accbest5=vailddigit(float(best5)/totalword)
    accbest10=vailddigit(float(best10)/totalword)
    print title[0],':','acc1:',accbest1,'acc5:',accbest5,'acc10:',accbest10


    # print feachline
