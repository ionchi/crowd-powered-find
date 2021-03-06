import random

M1 = 10
tresh1=0.5
tresh2=0.3
M=20
M2 = 10
TotalItems=1000000
K = 15
#Y0 = 30
errorRate = 0.35
selectivity = 0.2


def p_n1n2_if_true(n1, n2):
    return ((1 - errorRate) ** n1) * (errorRate ** n2)


def p_n1n2_if_false(n1, n2):
    return (errorRate ** n1) * ((1 - errorRate) ** n2)


def p_n1n2(n1, n2,):
    return selectivity * p_n1n2_if_true(n1, n2) + (1 - selectivity) * p_n1n2_if_false(n1, n2)


#la probabilità effettivamente è uno
def pr1n1n2(n1, n2):
    assert p_n1n2(n1, n2) != 0, 'Probability is not defined if P(n1, n2) = 0'
    return selectivity * p_n1n2_if_true(n1, n2) / p_n1n2(n1, n2)


#def pr0n1n2(n1, n2):
    #return 1 - pr1n1n2(n1, n2)

def pr0n1n2(n1, n2):
    assert p_n1n2(n1, n2) != 0, 'Probability is not defined if P(n1, n2) = 0'
    return (1-selectivity) * p_n1n2_if_false(n1, n2) / p_n1n2(n1, n2)


def p0(n1, n2):
    """
    the probability to observe a No if (n1, n2).
    we may estimate the probability to I=true, given (n1, n2).
    Knowing that I=true, the probability to get a "no" is the probability
    that the worker lie. (same for I=false)
    """
    return pr1n1n2(n1, n2) * errorRate + pr0n1n2(n1, n2) * (1 - errorRate)


def p1(n1, n2):
    return pr1n1n2(n1, n2) * (1 - errorRate) + pr0n1n2(n1, n2) * errorRate


def majority(n1, n2, M):
    if n1 == ((M + 1) / 2):
        return 1
    if n2 == ((M + 1) / 2):
        return 0
    return 2


def rectangular(n1, n2):
    if n1 == M1:
        return 1
    if n2 == M2:
        return 0
    return 2

def treshold(n1,n2):
    if tresh1 < tresh2:
        print("incorrect threshold configuration... will be reversed")
        treshapp1=tresh2
        treshapp2=tresh1
    else:
        treshapp1=tresh1
        treshapp2=tresh2

    if treshapp1<=pr1n1n2(n1,n2):
        return 1
    else:
        if treshapp2>pr0n1n2(n1,n2):
        #if treshapp1 < pr0n1n2(n1, n2):
            return 0
        else:
            return majority(n1,n2,M)








def Y(n1, n2, Y0, strategy=rectangular):
    if n1 == n2 == 0:
        return Y0
    if strategy(n1, n2) == 0:
        return Y0
    if strategy(n1, n2) == 1:
        return 0
    return min(Y0,
               1 + p1(n1, n2) * Y(n1 + 1, n2, Y0,  strategy=strategy)
               + p0(n1, n2) * Y(n1, n2 + 1, Y0, strategy=strategy))


def Y00():
    max_error = 1e-2
    max_iterations = 50
    found = False
    i = 0

    current_max = 500
    current_min = 0

    while not found:
        if i == max_iterations:
            raise Exception("Max Iterations")

        candidate_y00 = current_min + (current_max - current_min) / 2.0

        #ec = Y(0,0,candidate_y00)
        estimated_Y00 = 1 + p1(0, 0) * Y(1, 0,candidate_y00) + p0(0, 0) * Y(0, 1,candidate_y00)

        error = abs(estimated_Y00 - candidate_y00)
        print(
        "[i] trying Y(0, 0) = %s, estimated Y(0, 0) is %s with error: %s" % (
        str(candidate_y00), str(estimated_Y00), str(error)))

        found = error <= max_error

        if estimated_Y00 < candidate_y00:
            current_max = candidate_y00
        else:
            current_min = candidate_y00

        i += 1
    return candidate_y00


def inizializzazione(TotalItems, selectivity):
    Item=[]
    i=0
    while(i <= TotalItems):
        while(i <= TotalItems * selectivity):
            Item.append(1)
            i+=1
        Item.append(0)
        i+=1
    random.shuffle(Item)
    Strategy={}
    c=0
    while(c < TotalItems):
        Strategy[c]=[(0,0)]
        c+=1
    #print(Strategy)
    return Item, Strategy


def min2(Y,n,Strategy):

    app=Strategy.copy()
    lower=[]
    while len(lower) < n:
        low=99999
        for key in app:
            if (Y[app[key][0]]<low):
                low=Y[app[key][0]]
                chiave=key
        lower.append(chiave)
        del app[chiave]
    return lower





# Inizio MAIN

def main():

    Item, Strategy = inizializzazione(TotalItems, selectivity)
    Y0=Y00()
    l=[]
    y={}

    #u=Item.copy()
    app=[]

    #aggiorno elenco delle y note con i nuovi punti della strategia
    for key in Strategy:
        if(not Strategy[key] in app):
            app.append(Strategy[key])

    for ap in app:
        if(not ap[0] in y):
            y[ap[0]]=Y(ap[0][0], ap[0][1], Y0)

    fasi=0
    domande=0
    while(len(l)<K):
        fasi+=1
        I2=min2(y,K-len(l),Strategy)
        cq={}

        for i in I2:
            n1=M1-Strategy[i][0][0]
            n2=M2-Strategy[i][0][1]
            cq[i] =min(n1,n2)
            domande+=cq[i]

        for i in cq:
            c=0
            while(c<cq[i]):
                #simulo crowdsourcing
                if(random.random()>errorRate):
                    if(Item[i]==1):
                        a=Strategy[i][0][0]+1
                        b=Strategy[i][0][1]
                    else:
                        a = Strategy[i][0][0]
                        b = Strategy[i][0][1]+1
                    Strategy[i]=[(a,b)]
                else:
                    if (Item[i] == 1):
                        a = Strategy[i][0][0]
                        b = Strategy[i][0][1]+1
                    else:
                        a = Strategy[i][0][0]+1
                        b = Strategy[i][0][1]
                    Strategy[i] = [(a, b)]
                c+=1
        for i in cq:
            if rectangular(Strategy[i][0][0],Strategy[i][0][1])==1:
                l.append(i)
                del(Strategy[i])
            else:
                if rectangular(Strategy[i][0][0],Strategy[i][0][1])==0:
                    del(Strategy[i])
                else:
                    if not Strategy[i][0] in y:
                        y[Strategy[i][0]]=Y(Strategy[i][0][0], Strategy[i][0][1], Y0)

    print("oggetti")
    uni=0
    for p in l:
        if(Item[p]==1):
            uni+=1
        print(p,Item[p])

    accuracy=uni/len(l)
    print("accuracy: "+ str(accuracy)+"\n")
    print("risultato ottenuto in:\n"+"\tfasi: "+str(fasi)+"\n"+"\tdomande:"+str(domande) )

main()

