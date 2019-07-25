import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
def MCL(G3):
    G3=G3.astype(float)
    r=6#inflation constant
    for x in range(len(G3)): #self loop adding
        G3[x][x]=1.0
    
    for x in range(len(G3)):  #for normaliztion of matrix, after this sum of each row will be 1
        G3[x]=G3[x]/G3[x].sum()  #Delta^-1.Mt

    D=1.0
    co=0
    while (D>=0.00000001):
        O=G3
        G3=G3.dot(G3)   # Dot product n.n
        GP=np.power(G3,r)  # There we will raise each element with power of r( inflation constant)
        for x in range(len(G3)):
            G3[x]=GP[x]/GP[x].sum()   #divide each element by respactive row sum of matrix GP
            
        for x in range(len(G3)):   # These three steps are for float format conversion
            for y in range(len(G3)):
                G3[x][y]=float('{:.8f}'.format(G3[x][y]))
                
        D=G3-O
        D=np.power(D,2)
        D=np.sqrt(D.sum())
        co+=1
        print("\n\n",D,"\n\n",G3,"\n\n",co)
    elist=[]
    #for ploting the graph after MCL
    msg="from,to" # for writing the edge pairs to file
    for x in range(0,len(G3)): #both loop are for reading the simi matrix and making edge list 
        for k in range(x,len(G3)):
            if G3[x][k]!=0.0:
                elist.append([x,k,G3[x][k]])
                msg+=f"\n{x},{k},{G3[x][k]}"  # writing step

    #writing steps
    fobj=open('G3.csv','w')  #Write the msg where the format is as N1,N2
    fobj.write(msg)
    fobj.close()
    
    g2=nx.Graph()
    g2.add_weighted_edges_from(elist)
    nx.draw(g2)
    plt.show()

#graph=np.array([[1,1,0,1,0,1,0],[1,1,1,1,0,0,0],[0,1,1,1,0,0,1],[1,1,1,1,1,0,0],[0,0,0,1,1,1,1],[1,0,0,0,1,1,1],[0,0,1,0,1,1,1]]).astype(float)
