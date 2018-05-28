def expectedCost(n):
    #recursive function for computing the expected cost
    pass


def min2(Y):
    #compute the min value of the map
    pass


def computeN(i, S, param):
    pass


def CrowdSourcing(Q):
    pass


def ParallelCrowdSourcing(i, param):
    pass


def update(S, YesAns, NoAns):
    pass


def crowdfind(I,S,K,PR):
    l=0
    L=[]
    Y={} # expected cost of each Item
    u=[] #subset of I
    memory={} #memory of y cost


    for n in S.point:
        Y[n]=expectedCost(n)
        if n not in memory:
            memory[n]=Y.get(n)

    while(l<K):
        c=0
        while(c<(K-l)):
            u.append(min2(Y))
            c+=1
        #Q={}
        for i in u:
            n1=computeN(i,S,'Yes')
            n2=computeN(i,S,'No')
            #Q[i]=min(n1,n2)
            (YesAns,NoAns)=ParallelCrowdSourcing(i,min(n1,n2))
            S.update(YesAns,NoAns)
            if(S.result(i)):
                L.append(i)
                l+=1
            u.pop(i)


