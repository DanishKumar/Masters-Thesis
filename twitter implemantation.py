import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import mclmethod


#Markov Clustering
def MCL(G3):
    
    r=2.5 #inflation constant
    for x in range(len(G3)):
        G3[x][x]=1.0
    for x in range(len(G3)):  #for normaliztion of matrix, after this sum of each row will be 1
        G3[x]=G3[x]/G3[x].sum()  #Delta^-1.Mt
    D=1.0
    co=0
    while (D>=0.001):
        O=G3
        G3=G3.dot(G3)   # Multiply n.n
        GP=np.power(G3,r)  # There we will raise each element with power of r( inflation constant)
        for x in range(len(G3)):
            G3[x]=GP[x]/GP[x].sum()   #divide each element by respactive row sum of matrix GP
            
        for x in range(len(G3)): #formatting
            for y in range(len(G3)):
                G3[x][y]=float('{:.4f}'.format(G3[x][y]))
                        
                                      
                       
        D=G3-O
        D=np.power(D,2)
        D=np.sqrt(D.sum())
        co+=1
        print("\n\n",D,"\n\n",G3,"\n\n",co)

        elist=[]
    msg="from,to"
    for x in range(len(G3)):
        for z in range(len(G3)):
            if (G3[x][z]>0):
                msg+=f"\n{x+1},{z+1}"
                elist.append([x,y])

    fobj=open('MCL.csv','w')  #Write the msg where the format is as N1,N2
    fobj.write(msg)
    fobj.close()           

    g1=nx.Graph()
    g1.add_edges_from(elist)
    nx.draw(g1)
    plt.show()

#PreProcessing removes the punctuations and stopwords  
def text_procss(mess):
    ''' 
    1. remove punctuations
    2. reomve stopwords
    3. return list of clean list
    '''
    nopunc=[c for c in mess if c not in string.punctuation]
    nopunc=''.join(nopunc)
    stp=stopwords.words('english')
    extrastopwords=["games","made",'know','whos','role','lovely','two','us','way','work','wished','amp','youve','10th','morning'] #here we can add more stopwords other then default stopwords of english language
    stp.extend(extrastopwords)
    return ' '.join([word for word in nopunc.split() if word.lower() not in stp ])

#Use to create a list of hashtags
def hashtag(text):
    a=" "
    ht="n"
    import string
    for c in text: #reading each charachter
        
        if c=="#":  #if # is read so change ht flag to #
            ht="#"
        elif c==" ": #if space occured so word is compelte ht flag to space to stop writing any more
            ht=" "
        if ht=="#"and c not in string.punctuation:
            a=a+c
        elif ht==" " and a[-1]!=" ":
            a=a+" "
            ht="n" #used randomly to stop writing space symbole anymore
    return a.strip(" ")

#use to check the intersection of tweets having common tweets
def intersection(set1,set2):
    return [x for x in set1 if x in set2]

#use to remove links start with http
def removelink(text):
    msg=""
    textlist=text.lower().split(" ")
    for i in range(0,len(textlist)-1):
        if textlist[i].startswith("http"):
            del textlist[i]
    for i in textlist:
        msg=msg+i+" "
    return msg

corpus=[]
hashlist=[]

fobj=open("tweetssmall.txt")

for line in fobj:
    if line!="":
        hashlist.append(hashtag(line).rstrip("\n").lower().split(" "))
        corpus.append(removelink(text_procss(line.rstrip("\n"))))

fobj.close()
#readline and call Text_procss add it to the corpus


vectorizer=CountVectorizer()
r1=vectorizer.fit_transform(corpus)
r2=r1.toarray()
tf=r2.sum(axis=0)
print("\nTF Values\n")
print(tf)
print("\nVocabulary\n")
vocabulary=vectorizer.get_feature_names()
print(vocabulary)

transformer=TfidfTransformer()
tfidf=transformer.fit_transform(r2)
tfidf=tfidf.toarray().sum(axis=0)
#tfidf=tfidf.toarray()
#tfidf=tfidf.sum(axis=0)
#print("\nTf-idf values\n")
#print(tfidf)

dic={}
for x in range(0,len(vocabulary)):
    dic[vocabulary[x]]=tfidf[x]

#checking intersection of hashlist items, store result in matrix format node1,node2,no.of intersect hashtags

intersec=np.zeros(shape=(len(hashlist),len(hashlist)))
for x in range(0,len(hashlist)): #upper tringular matrix 
    for y in range(x+1,len(hashlist)):
                  intersec[x][y]=(len(intersection(hashlist[x],hashlist[y]))) #just checking how many common tags are there and add its len to the matrix 
                         
                         
#top 110 words list, sort the dic where we store word,tfidf pairs considering tfidf the select top 110 words and add them to a separte list topwords

import operator

topwords=[]

sorteddic=sorted(dic.items(),key=operator.itemgetter(1)) #sorting 

for x in range(len(dic)-110,len(dic)):
    topwords.append(sorteddic[x][0])


#creating nodes using topwords list
#read doc from corpus and the use loop take each word from topword list and compare with doc if aviable add 1 else 0 and make a list for each the add list to list nodes
nodes=[]
for x in corpus:
	a=[]
	for y in topwords:
		if y in x.lower().split():
			a.append(1.0) #float type 1.0
		else:
			a.append(0.0)
	nodes.append(a)
        

#distance formula we have nodes and edges in intersec
i=np.identity(len(topwords)).astype(float) #110 lenght
dist=np.zeros((len(nodes),len(nodes))).astype(float)
for x in range(0,len(nodes)):
    for y in range(x+1,len(nodes)):
        lemda1=1.0/(1.0+float(intersec[x][y]))
        r1=np.sqrt(np.transpose(np.array(nodes[x])-np.array(nodes[y])).dot(lemda1*(i)).dot(np.array(nodes[x])-np.array(nodes[y])))
        dist[x][y]=r1

#similarity graph
sim=np.zeros((len(dist),len(dist)))
for x in range(0,len(dist)-1):
            sim[x]=1.0-(dist[x]/np.max(dist[x])) #be careful here the lower tringular is 1 as it was zero so 1-0=1, so we have to not use low tringular values
for x in range(0,len(sim)):
    for y in range(x+1,len(sim)):
        if sim[x][y]>0.1:
            sim[y][x]=sim[x][y]=sim[x][y]
        else:
            sim[y][x]=sim[x][y]=0.0
            
            
#creating elist of the similarity graph, will help us in viualisation of the graph and further we can use this to feed it to the MCL
#here we can use thrshold value to add edge or not
elist=[]
xx=0
for x in range(0,len(sim)):
    for y in range(x+1,len(sim)):
        elist.append((x,y,sim[x][y]))
        if sim[x][y]>0:
            xx+=1

#using networkx library for drawing the graph

graph=nx.Graph()
graph.add_weighted_edges_from(elist)
nx.draw(graph)
plt.show()

sim=sim.astype(float)
sim1=sim
#MCL(sim)
mclmethod.MCL(sim)
