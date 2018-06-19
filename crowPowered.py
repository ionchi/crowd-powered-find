import random

M1 = 10
M2 = 10
TotalItems=2000
K = 15
Y0 = 59
errorRate = 0.35
selectivity = 0.2

def p_n1n2_if_true(n1, n2, errorRate):
    return ((1 - errorRate) ** n1) * (errorRate ** n2)


def p_n1n2_if_false(n1, n2, errorRate):
    return (errorRate ** n1) * ((1 - errorRate) ** n2)


def p_n1n2(n1, n2, true_a_priori, errorRate):
    return true_a_priori * p_n1n2_if_true(n1, n2, errorRate) + (1 - true_a_priori) * p_n1n2_if_false(n1, n2, errorRate)


#la probabilità effettivamente è uno
def pr1n1n2(n1, n2, true_a_priori, errorRate):
    assert p_n1n2(n1, n2, true_a_priori, errorRate) != 0, 'Probability is not defined if P(n1, n2) = 0'
    return true_a_priori * p_n1n2_if_true(n1, n2, errorRate) / p_n1n2(n1, n2, true_a_priori, errorRate)


def pr0n1n2(n1, n2, true_a_priori, errorRate):
    return 1 - pr1n1n2(n1, n2, true_a_priori, errorRate)


def p0(n1, n2, a_priori, errorRate):
    """
    the probability to observe a No if (n1, n2).
    we may estimate the probability to I=true, given (n1, n2).
    Knowing that I=true, the probability to get a "no" is the probability
    that the worker lie. (same for I=false)
    """
    return pr1n1n2(n1, n2, a_priori, errorRate) * errorRate + pr0n1n2(n1, n2, a_priori, errorRate) * (1 - errorRate)


def p1(n1, n2, a_priori, errorRate):
    return pr1n1n2(n1, n2, a_priori, errorRate) * (1 - errorRate) + pr0n1n2(n1, n2, a_priori, errorRate) * errorRate


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


def Y(n1, n2, Y0, errorRate, a_priori, strategy=rectangular):
    if n1 == n2 == 0:
        return Y0
    if strategy(n1, n2) == 0:
        return Y0
    if strategy(n1, n2) == 1:
        return 0
    return min(Y0,
               1 + p1(n1, n2, a_priori, errorRate) * Y(n1 + 1, n2, Y0, errorRate=errorRate, a_priori=a_priori, strategy=strategy)
               + p0(n1, n2, a_priori, errorRate) * Y(n1, n2 + 1, Y0, errorRate=errorRate, a_priori=a_priori, strategy=strategy))


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


def Y00():
    alfa=150
    esup=500
    emin=0
    bol=False
    while(bol is False):
        prova=Y(0,0,alfa)
        print(prova)
        if(alfa>prova):
            esup=alfa
            alfa=int((esup-emin)/2)
        else:
            if(alfa<prova):
                emin=alfa
                alfa=int((esup-emin)/2)
            else:
                if(alfa==prova):
                    bol=True
        print(alfa)

#Y00()


# Inizio MAIN

Item, Strategy = inizializzazione(TotalItems, selectivity)

strategy2=Strategy.copy()
l=[]
u=[]
y={}

u=Item.copy()
app=[]

#aggiorno elenco delle y note con i nuovi punti della strategia
for key in Strategy:
    if(not Strategy[key] in app):
        app.append(Strategy[key])

for ap in app:
    if(not ap[0] in y):
        y[ap[0]]=Y(ap[0][0], ap[0][1], Y0, errorRate, selectivity)

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
                    y[Strategy[i][0]]=Y(Strategy[i][0][0], Strategy[i][0][1], Y0, errorRate, selectivity)

print("oggetti")
uni=0
for p in l:
    if(Item[p]==1):
        uni+=1
    print(p,Item[p])

print(uni/len(l))
print("risultato ottenuto in:\n"+"\tfasi: "+str(fasi)+"\n"+"\tdomande:"+str(domande) )

# Fine MAIN
