from Strategy import *
from punto import *
from Crowfind import *
from Item import *
from random import randint

i=0
n=10
K=3
I=[]
a={}

while (i<n):
    I.append(Item(i, randint(0, 1)))
    a[i]=points(i,i*2)
    i+=1
S=Strategy(a,1)

crowdfind(I,S,K,1)
