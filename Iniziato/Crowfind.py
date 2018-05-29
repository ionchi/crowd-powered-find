def expectedCost(n):
    #recursive function for computing the expected cost
    pass


def min2(Y,n):

    lower=[]
    while(len(lower)<n):
        low=99999
        for key, value in Y.items():
            if (value < low):
                low=value
                chiave=key
        lower.append(low)
        del Y[chiave]
        low=99999
    return lower


def computeN(i, S, param):
    pass


def CrowdSourcing(Q):
    pass


def ParallelCrowdSourcing(i, param):
    pass



def crowdfind(I,S,K,PR):
    l=0
    L=[]
    Y={} # expected cost of each Item
    u=[] #subset of I
    memory={} #memory of y cost

    for n in S.points:


        Y[n]=expectedCost(S.points[n])
        if n not in memory:
            memory[n]=Y.get(n)



    while(l<K):
        u.extend(min2(Y,K-l))
        Q={}
        for i in u:
            n1=computeN(i,S,'Yes')
            n2=computeN(i,S,'No')
            Q[i]=min(n1,n2)
            (YesAns,NoAns)=ParallelCrowdSourcing(i,min(n1,n2))
            S.updateS(3,1,i)
            if(S.actuateStrategy()==1):
                L.append(i)
                l+=1
                u.pop(i)
            else:
                if(S.actuateStrategy()==0):
                    u.pop(i)





