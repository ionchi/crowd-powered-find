

class Strategy(object):

    def __init__(self,points,Strategia):
        self.points=points
        self.Strategia= Strategia

    def updateS(self,a,b,i):
        self.points[i].n1+=a
        self.points[i].n2+=b

    def __str__(self):
        a=''
        for key, value in self.points.items():
            a+=str(key)+": "+"("+str(self.points[key].n1)+","+str(self.points[key].n2)+")"+'\n'
        return ''+a+ " "

    def actuateStrategy(self,i,a,b,c,pr):
        if (self.Strategia==1):
            if(self.points[i].n1+self.points[i].n2==a):
                soglia=(a+1)/2
                if(self.points[i].n1>soglia):
                    return 1
                if (self.points[i].n2 > soglia):
                    return 0
            else:
                return 2
        if(self.Strategia==2):
            if(self.points[i].n1>=a):
                return 1
            else:
                if(self.points[i].n2>=b):
                    return 0
                else:
                    return 2
        return 2
        #if(self.Strategia==3):
           #qualcosa nel paper non torna









