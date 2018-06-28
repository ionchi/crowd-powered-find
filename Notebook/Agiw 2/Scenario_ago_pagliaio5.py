import random

#inseriamo domande con risposta facile per alzare attenzione INSERITO
#vari utenti che a ogni fase quando dimunuisco utenti caccio quelli che sono peggiori, vanno gestiti i peggiori o miglio NON INSERITO



M1 = 10
tresh1=0.5
tresh2=0.3
M=20
M2 = 10
ermax=0.45
TotalItems=100000
taskdiff=0.1
taskmed=0.2
tasknormal=0.7

#errorRate = 0.1

selectivity = 0.001
#K=TotalItems*selectivity
K=20
#errorRate1=0.3
#errorRate0=selectivity



def p_n1n2_if_true(n1, n2,errorRate1,errorRate0):
    return ((1 - errorRate1) ** n1) * (errorRate0 ** n2)


def p_n1n2_if_false(n1, n2,errorRate1,errorRate0):
    return (errorRate1 ** n1) * ((1 - errorRate0) ** n2)


def p_n1n2(n1, n2,errorRate1,errorRate0):
    return selectivity * p_n1n2_if_true(n1, n2,errorRate1,errorRate0) + (1 - selectivity) * p_n1n2_if_false(n1, n2,errorRate1,errorRate0)


#la probabilità effettivamente è uno
def pr1n1n2(n1, n2,errorRate1,errorRate0):
    assert p_n1n2(n1, n2,errorRate1,errorRate0) != 0, 'Probability is not defined if P(n1, n2) = 0'
    return selectivity * p_n1n2_if_true(n1, n2,errorRate1,errorRate0) / p_n1n2(n1, n2,errorRate1,errorRate0)


#def pr0n1n2(n1, n2):
    #return 1 - pr1n1n2(n1, n2)

def pr0n1n2(n1, n2,errorRate1,errorRate0):
    assert p_n1n2(n1, n2,errorRate1,errorRate0) != 0, 'Probability is not defined if P(n1, n2) = 0'
    return (1-selectivity) * p_n1n2_if_false(n1, n2,errorRate1,errorRate0) / p_n1n2(n1, n2,errorRate1,errorRate0)


def p0(n1, n2,errorRate1,errorRate0):
    """
    the probability to observe a No if (n1, n2).
    we may estimate the probability to I=true, given (n1, n2).
    Knowing that I=true, the probability to get a "no" is the probability
    that the worker lie. (same for I=false)
    """
    return pr1n1n2(n1, n2,errorRate1,errorRate0) * errorRate1 + pr0n1n2(n1, n2,errorRate1,errorRate0) * (1 - errorRate0)


def p1(n1, n2,errorRate1,errorRate0):
    return pr1n1n2(n1, n2,errorRate1,errorRate0) * (1 - errorRate1) + pr0n1n2(n1, n2,errorRate1,errorRate0) * errorRate0


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

    if treshapp1<pr1n1n2(n1,n2):
        return 1
    else:
        if treshapp2>pr0n1n2(n1,n2):
            return 0
        else:
            return majority(n1,n2,M)








def Y(n1, n2, Y0,errorRate1,errorRate0, strategy=rectangular):
    if n1 == n2 == 0:
        return Y0
    if strategy(n1, n2) == 0:
        return Y0
    if strategy(n1, n2) == 1:
        return 0
    return min(Y0,
               1 + p1(n1, n2,errorRate1,errorRate0) * Y(n1 + 1, n2, Y0,errorRate1,errorRate0, strategy=strategy)
               + p0(n1, n2,errorRate1,errorRate0) * Y(n1, n2 + 1, Y0, errorRate1,errorRate0, strategy=strategy))


def Y00():
    max_error = 1e-2
    max_iterations = 50
    found = False
    i = 0

    current_max = 5000000000
    current_min = 0

    while not found:
        if i == max_iterations:
            return candidate_y00

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
    Item2={}
    i=0
    cont1=0
    cont2=0
    cont3=0
    while i < TotalItems:
        a=random.random()
        if (a>=(1-tasknormal)):
            #se compreso tra 0.3 e 1 nel caso 0.7
            Item2[i]=1
            cont1+=1
        else:
            if (a>taskdiff):
                #se compreso tra 0.1 e 0.3
                Item2[i]=2
                cont2 += 1
            else:
                #se minore uguale alla probabilità che sia difficile
                Item2[i]=3
                cont3 += 1
        i+=1
    while(c < TotalItems):
        Strategy[c]=[(0,0)]
        c+=1
    #print(Strategy)
    print("task facili: " + str(cont1)+"\n"+"task medi: " + str(cont2) + "\n"+"task difficili: "+str(cont3))
    return Item, Strategy,Item2


def min2(Y_store, n, Strategy):

    app=Strategy.copy()
    lower=[]
    while len(lower) < n and len(app)>0:
        low=99999
        for key in app:
            if (Y_store[app[key][0]]<low):
                low=Y_store[app[key][0]]
                chiave=key
        lower.append(chiave)
        del app[chiave]
    #print(lower)
    return lower

def min3(Utenti,n):
    app=Utenti.copy()
    while len(app) > n:
        max=0
        for key in app:
            if (app[key]>max):
                max=app[key]
                chiave=key
        del app[chiave]
    #print (app)
    return app







# Inizio MAIN

UtSpammer=0.25
UtMedi=0.5
UtHammer=0.25
Pspammer=0.42
PNormal=0.3
Phammer=0.1

def utenti(n):
    Spammer=int(UtSpammer*n)
    Normal=int(UtMedi*n)
    Hammer=int(UtHammer*n)
    Somma=Hammer+Spammer+Normal
    if Somma<n:
        a=n-Somma
        Normal+=a
    ut={}
    c=0
    i=0
    while(i<Spammer):
        ut[c]=Pspammer
        c+=1
        i+=1
    i=0
    while(i<Normal):
        ut[c]=PNormal
        c+=1
        i+=1
    i=0
    while(i<Hammer):
        ut[c]=Phammer
        c+=1
        i+=1
    return ut




def main():



    Item, Strategy,Item2 = inizializzazione(TotalItems, selectivity)
    #attention=20
    Y0=50000
    #print(Y0)
    domande0=0
    #domandeextra=0
    #fasiextra=0
    domande1=0
    errorRate0 = selectivity
    #errorRate = 0.25
    fasciamed=0.05
    fasciadiff=0.1
    l=[]
    scartati=0
    y={}

    nutenti = K * M1
    Utenti = utenti(nutenti)
    errorRate=Pspammer*UtSpammer+PNormal*UtMedi+Phammer*UtHammer
    #u=Item.copy()
    app=[]

    #aggiorno elenco delle y note con i nuovi punti della strategia
    for key in Strategy:
        if(not Strategy[key] in app):
            app.append(Strategy[key])


    for ap in app:
        if(not ap[0] in y):
            y[ap[0]]=Y(ap[0][0], ap[0][1], Y0,errorRate,errorRate0)


    fasi=0
    domande=0
    #errorRate1=errorRate
    while(len(l)<K and len(Strategy)>0):

        errorRate=0
        for i in Utenti:
            errorRate+=Utenti[i]
        errorRate=errorRate/len(Utenti)

        fasi+=1
        for ut in Utenti:
            if Utenti[ut]<=ermax:
                if fasi%200==0:
                    #print("yes")
                    nnn=fasi/200
                    Utenti[ut]=Utenti[ut]+nnn*0.005
                    #print(errorRate1)


        I2=min2(y,K-len(l),Strategy)
        cq={}
        domandefase=0
        for i in I2:
            n1=M1-Strategy[i][0][0]
            n2=M2-Strategy[i][0][1]
            cq[i] =min(n1,n2)
            domande+=cq[i]
            domandefase+=cq[i]


        #if fasi%attention:
         #   for i in cq:
          #      domande+=cq[i]
           #     domandeextra+=cq[i]
            #fasiextra+=1

        Utenti2=min3(Utenti,domandefase)
        #print(Utenti)
        listakey=Utenti2.keys()
        b=[]
        for i in listakey:
            b.append(int(i))
        b2=b.copy()
        #print(len(b2))
        #print(Utenti)
        for i in cq:
            c=0

            while(c<cq[i]):
                #simulo crowdsourcing
                #if(random.random()>errorRate):
                prut=b2.pop(0)
                errorRate1=Utenti[prut]
                app2=errorRate0
                if(Item[i]==1):
                    if(Item2[Item[i]]==2):
                        errorRate1+=fasciamed
                    if(Item2[Item[i]]==3):
                        errorRate1+=fasciadiff

                    if(random.random()<=errorRate1):
                        a=Strategy[i][0][0]
                        b=Strategy[i][0][1]+1
                        Utenti[prut]=Utenti[prut]+0.01
                    else:
                        a = Strategy[i][0][0]+1
                        b = Strategy[i][0][1]
                        Utenti[prut] = Utenti[prut] - 0.01
                    Strategy[i]=[(a,b)]
                    domande1+=1
                else:
                    if (Item2[Item[i]] == 2):
                        errorRate0 += fasciamed
                    if (Item2[Item[i]] == 3):
                        errorRate0 += fasciadiff
                    if (random.random()<=errorRate0):
                        a = Strategy[i][0][0]+1
                        b = Strategy[i][0][1]
                    else:
                        a = Strategy[i][0][0]
                        b = Strategy[i][0][1]+1
                    Strategy[i] = [(a, b)]
                    domande0+=1

                errorRate0=app2
                c+=1

        for i in cq:
            if rectangular(Strategy[i][0][0],Strategy[i][0][1])==1:
                l.append(i)

                del(Strategy[i])
            else:
                if rectangular(Strategy[i][0][0],Strategy[i][0][1])==0:
                    if (Item[i] == 1):
                        scartati+=1
                    del(Strategy[i])
                else:
                    if not Strategy[i][0] in y:
                        y[Strategy[i][0]]=Y(Strategy[i][0][0], Strategy[i][0][1], Y0,errorRate,errorRate0)
        #print(len(Strategy))
        #print(len(l))

    #print("oggetti")
    uni=0
    for p in l:
        if(Item[p]==1):
            uni+=1
        #print(p,Item[p])

    accuracy=(uni/len(l))
    avg0=domande0/(TotalItems-len(Strategy)-len(l))
    avg1=domande1/len(l)
    recall=len(l)/(scartati+len(l))

    print(""+"numero di domande medio per elementi che non soddisfano proprietà: " +str(avg0) +"\n" )
    print("" + "numero di domande medio per elementi che soddisfano proprietà: " + str(avg1)+"\n")
    print("accuracy: " + "\n\tPrecision: "+str(accuracy)+"\n\tRecall: "+ str(recall)+"\n\tScartati: "+ str(scartati))
    print("risultato ottenuto in:\n"+"\tfasi: "+str(fasi) +
          "\n"+"\tdomande:"+str(domande) )


    #main()