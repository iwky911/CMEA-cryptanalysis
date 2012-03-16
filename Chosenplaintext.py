#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CMEA import *

class Decrypter:
    
    def __init__(self):
        print "init"
        self.knowntext=[]
        self.constraints = []
        self.known={}
    
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

    def getallconstraints(self, t0):
        for i in range(1,256):
            self.getconstraints(i, t0)
    
    def getconstraints(self, j, t0):
        n = self.c.blocksize
        P = [ (1- t0) % 256 for i in range(n)]
        k = (((n-1)^j) - (n-2)) % 256
        P[-1] = 0
        P[-2] = (k-t0) %256
        C = self.c.crypt(P)
        
        Pp=[1 for i in range(n-2)]
        Pp[-1]=k
        for i in range(len(Pp)/2):
            Pp[i]=Pp[i]^(P[len(Pp)-1-i] | 1)
        
        tjm = (C[0]+t0) % 256
        z=[0,tjm]
        for i in range(1, n-1):
            self.known[z[i] ^ i] = (Pp[i-1]-C[i]) % 256
            print "affect: ", self.c.Tbox(z[i]^i), self.known[z[i]^i]
            z.append((z[i]+ Pp[i-1])%256)
        
        self.constraints.append((C[-1], tjm, j, z[-1] ^ (n-1)))
    
    def solveconstraints(self):
        compteur = 0
        for (c, tj, j, z) in self.constraints:
            if j in self.known:
                if not z in self.known:
                    compteur+=1
                self.known[z] = (self.known[j] - c) %256
                print "affect:", self.known[z], self.c.Tbox(z)
            else:
                if z in self.known:
                    if not j in self.known:
                        compteur+=1
                    self.known[j] = (c + self.known[z]) % 256
                    print "affect: ",j, tj, self.known[j], self.c.Tbox(j)
                else:
                    posj = [tj, tj+1]
                    posz = [(tj-c)%256 , (tj+1 -c )%256]
                    posj = [k for k in posj if (k-j) %256 in cavetable]
                    posz = [k for k in posz if (k-z) %256 in cavetable]
                    #if len(posj)==1:
                     #   self.known[j] = posj[0]
                     #   print "affect:", self.known[j], self.c.Tbox(j)
                    #if len(posz)==1:
                      #  self.known[z] = posz[0]
                      #  print "affect:", self.known[z], self.c.Tbox(z)
        
        return compteur
                    
    
if __name__ == '__main__':
    d = Decrypter()
    d.setCrypter(CMEA())
    d.c.blocksize = 4
    d.c.createRandomKey()
    possibilities= d.findTzero()
    
    for p in possibilities:
        t = d.findPossibleOthers(p)
        if t != []:
            break
    print len([l for l in t if len(l)==2])
    
    d.getallconstraints(t[0][0])
    print len(d.known)
    print [(d.c.Tbox(i),d.known[i]) for i in d.known]
   # for i in range(10):
    #    d.solveconstraints()
    d.solveconstraints()
    print len(d.known)
    print [(d.c.Tbox(i),d.known[i]) for i in d.known]
    #for (c,tj,j,z) in d.constraints:
     #   print d.c.Tbox(j), d.c.Tbox(z), (d.c.Tbox(j)-d.c.Tbox(z)) % 256 , c, tj
