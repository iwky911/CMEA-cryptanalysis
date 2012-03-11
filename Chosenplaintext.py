#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CMEA import *

class Decrypter:
    
    def __init__(self):
        print "init"
        self.knowntext=[]
    
    def setCrypter(self, crypt):
        self.c=crypt
    
    def findTzero(self):
        s = set()
        for c in cavetable:
            s.add(c)
        possibility = set()
        for i in s:
            P = [(1-i)%256 for k in range(self.c.blocksize)]
            S = self.c.crypt(P)
            self.knowntext.append((P,S))
            if S[0] == (-i %256):
                possibility.add(i)
        return possibility

    def findPossibleOthers(self, t0):
        T = [[] for i in range(256)]
        r = random.Random()
        T[0].append(t0)
        for j in range(1,256):
            n = self.c.blocksize
            k = (((n-1)^j) - (n-2)) % 256
            
            P = [(1-t0) % 256 for i in range(n)]
            P[-1] = 0
            P[-2] = (k-t0) % 256
            C = self.c.crypt(P)
            self.knowntext.append((P,C))
            guess = (C[0] + t0) % 256
            if(not (guess-j)%256 in cavetable and not (guess-j+1)%256 in cavetable):
                #print "pas ",t0
                return []
            else:
                if (guess-j) %256 in cavetable:
                    T[j].append((guess) % 256)
                if ((guess-j)%256+1) in cavetable:
                    T[j].append((guess+1)%256)
        return T
    
    def Tbox(self,i, d):
        if i in d:
            return [d[i]]
        else:
            return self.t[i]

    def findExactTboxOutput(self,i):
        for i in range(t):
            pass

    def schema(self, d):
        self.d = 0
        
    def aux1(self, P,Pp,C,i,y,d):
        for k in self.Tbox(i^y[i],d):
            dp = d.copy()
            dp[i ^y[i]] = k
            Pp.append((P[i] + k) % 256)
            y.append((y[i] + Pp[i]) % 256)
            i+=1
            if(i==len(P)):
                (res, dic) = self.secondstep(Pp,C, dp)
            else:
                (res,dic) = self.aux1(P,Pp,C,i,y,dp)
            if res:
                return (res, dic)
            else:
                Pp.pop()
                y.pop()
                i-=1
        return (False, {})
                
    
    def firststep(self, P, C):
        return self.aux1(P,[],C,0,[0],{})
    
    def secondstep(self, Pp, C, d):
        Ppp =[]
        for i in range( len(P)/2):
            Ppp.append(Pp[i] ^ (Pp[len(P)-i-1] | 1))
        
        for i in range(len(P)/2, len(P)):
            Ppp.append(Pp[i])
        return self.thirdstep(Ppp, C, d)
        
    def thirdstep(self, Ppp, C, d):
        z=[0]
        c=[]
        return self.aux3(Ppp, C, z,0, c, d)
        
    def aux3(self,Ppp, C, z,i, c, d):
        for k in self.Tbox(i^z[i],d):
            dp = d.copy()
            #print i, z
            dp[i ^z[i]] = k
            z.append((z[i]+Ppp[i]) % 256)
            c.append((Ppp[i] - k) % 256)
            i+=1
            if(i==len(Ppp)):
                #print c
                if(False in [C[k] == c[k] for k in range(len(C))]):
                 #   print "echec"
                    (res,dic)=  (False, {})
                else:
                    (res, dic)=  (True, dp)
            else:
                (res,dic) = self.aux3(Ppp,C,z,i,c,dp)
            if res:
                return (res, dic)
            else:
                c.pop()
                z.pop()
                i-=1
        return (False, {})

if __name__ == '__main__':
    d = Decrypter()
    d.setCrypter(CMEA())
    d.c.blocksize = 3
    d.c.createRandomKey()
    possibilities= d.findTzero()
    
    for p in possibilities:
        t = d.findPossibleOthers(p)
        if t != []:
            break
    print len([l for l in t if len(l)==2])
    d.t=t
    #d.knowntext.extend([(a,b) for (b,a) in d.knowntext])
    r = random.Random()
    for i in range(100000):
        C = [r.randint(0,256) for i in range(d.c.blocksize)]
        d.knowntext.append((C, d.c.crypt(C)))
    proba = {}
    for (C,P) in d.knowntext:
        (res, dic) = d.firststep(P,C)
        for entree in dic:
            if not entree in proba:
                proba[entree] = {}
            if not dic[entree] in proba[entree]:
                proba[entree][dic[entree]]=0
            proba[entree][dic[entree]]+=1
    
    for a in proba:
        i = proba[a].keys()[0]
        for k in proba[a]:
            i=k if proba[a][k]>proba[a][i] else i
        
        if not d.c.Tbox(a)== i:
            print False
        
