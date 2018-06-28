import random
import os

HEADER = "Item,K,M1,M2,selectivity,errorRate,accuracy_avg,accuracy_lower,accuracy_higher,phases_avg,phases_lower,phases_higher" \
         ",questions_avg,questions_lower,questions_higher"
OUTPUT_FILE = "dataset_selettivita bassaerrorealto.csv"

if (os.path.exists(OUTPUT_FILE)):
    os.remove(OUTPUT_FILE)
    print("Removed: " + OUTPUT_FILE)
dataset = open(OUTPUT_FILE, "w")
print("Created empty file: " + OUTPUT_FILE)
dataset.write(HEADER + "\n")


TotalItems=100000
M1=15
M2=15
K=15

errorRate=0.4
selectivity=0.01
tresh1=0.5
tresh2=0.3
nfasi=20
M=20
cccc=0

y = {}

def p_n1n2_if_true(n1, n2):
    return ((1 - errorRate) ** n1) * (errorRate ** n2)
def p_n1n2_if_false(n1, n2):
    return (errorRate ** n1) * ((1 - errorRate) ** n2)
def p_n1n2(n1, n2,):
    return selectivity * p_n1n2_if_true(n1, n2) + (1 - selectivity) * p_n1n2_if_false(n1, n2)
def pr1n1n2(n1, n2):
    assert p_n1n2(n1, n2) != 0, 'Probability is not defined if P(n1, n2) = 0'
    return selectivity * p_n1n2_if_true(n1, n2) / p_n1n2(n1, n2)
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

    if treshapp1<pr1n1n2(n1,n2):
        return 1
    else:
        if treshapp2>pr0n1n2(n1,n2):
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


Y0 = Y00()


def main():
    print("main")

    Item, Strategy = inizializzazione(TotalItems, selectivity)


    l=[]


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

    uni=0
    for p in l:
        if(Item[p]==1):
            uni+=1


    accuracy=(uni/len(l))
    return accuracy,fasi,domande
accuracy_low=2
accuracy_high=-1
fasi_low=99999999
fasi_high=0
domande_low=999999999999
domande_high=0
count_master = 0
accuracy_sum=0
fasi_sum=0
domande_sum=0
while (count_master < nfasi):
    accuracy,fasi,domande=main()
    #aggiornamento per media
    accuracy_sum+=accuracy
    fasi_sum+=fasi
    domande_sum+=domande
    if accuracy>accuracy_high:
        accuracy_high=accuracy
    if accuracy<accuracy_low:
        accuracy_low=accuracy
    if fasi>fasi_high:
        fasi_high=fasi
    if fasi<fasi_low:
        fasi_low=fasi
    if domande>domande_high:
        domande_high=domande
    if domande<domande_low:
        domande_low=domande
    count_master+=1
    print(count_master)
accuracy_avg=accuracy_sum/nfasi
domande_avg=domande_sum/nfasi
fasi_avg=fasi_sum/nfasi
row=""+str(TotalItems)+","+str(K)+","+str(M1)+","+str(M2)+","+str(selectivity)+","+str(errorRate)+","+str(accuracy_avg)+","+str(accuracy_low)+","+str(accuracy_high)+","+str(fasi_avg)+","+str(fasi_low)+","+str(fasi_high)+","+str(domande_avg)+","+str(domande_low)+","+str(domande_high)+","
print(row)
cccc+=1
print(cccc)
dataset.write(row + "\n")
dataset.close()
print("File closed: " + OUTPUT_FILE)

