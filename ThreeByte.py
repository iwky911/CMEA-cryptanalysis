#!/usr/bin/python
#-*- coding:utf-8 -*-

from CMEA import *
from threading import Thread
import random

class CVInverse:
    def __init__(self):
        self.table = {}
        for i in range(256):
            self.table[i] = []
        for i in range(256):
            self.table[cavetable[i]].append(i)
    
    def getinverse(self, i):
        return self.table[i]

class Cryptanalysis3B:
    def __init__(self):
        nbplaintext = 90
        self.p0 = [ [ True for i in range(256) ] for j in range(256) ]
        for i in range(256):
            for j in range(256):
                if(not ((j-i) % 256) in cavetable):
                    self.p0[i][j] = False
        
        self.CVI = CVInverse()
        self.p = None
        
        self.c = CMEA()
        self.texts = self.createPlaintexts(nbplaintext, self.c)
        
    def getY1Z1(self, x, P, C):
        return (P[0] + x) % 256, (C[0] + x) % 256
        
    def checkValue(self, T0, p, P, C):
        y1, z1 = self.getY1Z1(T0, P, C)
        change = False
        for guess in range(256):
            if(p[y1 ^ 1][guess]):
            #if(guess == c.Tbox(y1 ^ 1)):
                #T(y1 ^ 1) = guess
                Pp1 = (P[1] + guess) % 256
                #P'(1) == P'(n-2)
                Ppp1 = Pp1 % 256
                #Tz1 -> T(z1 ^ 1)
                Tz1 = (Ppp1 - C[1]) % 256
                y2 = (y1 + Pp1) % 256
                z2 = (z1 + Ppp1) % 256
                #P'2 avec ambiguité sur le LSB
                Pp0 = (P[0] + T0) % 256
                Pp2 = (Pp0 ^ (C[0] + T0)) % 256
                #C[0] + T0 = Ppp0
                
                #T(y2 ^ 2) sauf LSB
                Ty20 = (Pp2 - P[2]) % 256
                Ty21 = ((Pp2 ^ 1) - P[2]) % 256
                Ppp2 = Pp2 % 256
                
                #T(z2 ^ 2) sauf LSB
                Tz20 = (Ppp2 - C[2]) % 256
                Tz21 = ((Ppp2 ^ 1) - C[2]) % 256
                
                """print "Pp1", Pp1
                print "Ppp1", Ppp1
                print "Pp0", Pp0
                print "Pp2", Pp2
                print "y1", y1
                print "y2", y2
                print "z1", z1
                print "z2", z2
                print "Ty20", Ty20
                print "Ty21", Ty21"""
                
                if(not p[z1 ^ 1][Tz1]):
                    p[y1 ^ 1][guess] = False
                    change = True
                if((not p[y2 ^ 2][Ty20] or not p[z2 ^ 2][Tz20]) and (not p[y2 ^ 2][Ty21] or not p[z2 ^ 2][Tz21])):
                    p[y1 ^ 1][guess] = False
                    change = True
                    
        return change
    
    def buildP(self):
        self.p0 = [ [ True for i in range(256) ] for j in range(256) ]
        for i in range(256):
            for j in range(256):
                if(not ((j-i) % 256) in cavetable):
                    p0[i][j] = False
        
    def copyP(self):
        p = [ q[:] for q in self.p0 ]
        return p
        
                
    def checkT0Value(self,x):
        p = self.copyP()
        continuer = True
        while(continuer):
           # print "iter"
            continuer = False
            for (P, C) in self.texts:
              #  print [ len([k for k in t if k!=0]) for t in p]
                continuer = continuer or self.checkValue(x, p, P, C)
            for (C, P) in self.texts:
                continuer = continuer or self.checkValue(x, p, P, C)
            for i in range(256):
                if(not (True in p[i])):
                    return False
        self.p = p
        return True
        
    def findT0(self):
        for x in range(256):
            if(x in cavetable and self.checkT0Value(x)):
                print x, "good!"
                self.myt0=x
            else:
                print x, " not good"
      
    def findT0parallel(self):
        n = 8
        threadlist = []
        for i in range(n):
            t = range(i*256/n, (i+1)*256/n)
            threadlist.append(Parallel(t,self.c ,self.texts, self))
        
        for t in threadlist:
            t.start()
        
        sortie = []
        for t in threadlist:
            t.join()
            sortie.extend(t.l)
        self.myt0=sortie[0]
        
    def createPlaintexts(self, n, c, size=3):
        r = random. Random()
        l = []
        #c.createRandomKey()
        print "t0", c.Tbox(0)
        c.blocksize = size
        for i in range(n):
            P=[r.randint(0,255) for k in range(size)]
            #P = [45, 89, 23]
            l.append((P, c.crypt(P)))
        return l
    
    def getPossible67values(self):
        s = set()
        possible = []
        for k in cavetable:
            s.add(k)
        
        for k6 in xrange(256):
            for k7 in xrange(256):
                exit=False
                if k7 ==0:
                    print k6
                    
                broke=False
                for i in range(256):
                    jfound=False
                    for ctv in s:
                        j = (i+ cavetable[(((ctv+i)^k6)+k7)%256])%256
                        if(self.p[i][j]):
                            jfound=True
                        
                    if not jfound:
                        broke = True
                        break
    
                if not broke:
                    possible.append((k6,k7))
            
        self.possible67 = possible
    
    def get4tuples(self):
        sortie = []
        for i in range(256):
            t = [k for k in range(256) if self.p[i][k]==True]
            if len(t)==1:
                sortie.append((i, t[0]))
        self.tuples = sortie[:4]
    
    def calcp(self, x, k0, k1, k2):
        return ((cavetable[((x^k0)+k1) %256] +x)^k2) %256
    
    def createHashTableprime(self):
        self.startmap = {}
        for k0 in xrange(256):
            print k0
            for k1 in xrange(256):
                for k2 in xrange(256):
                    tp = [self.calcp(x, k0, k1 ,k2) for (x, tx) in self.tuples]
                    n = [(p - tp[3]) %256 for p in tp[:3]]
                    n = n[0]*256**2+n[1]*256+n[2]
                    if not n in self.startmap:
                        self.startmap[n]=[]
                    self.startmap[n].append([k0,k1,k2, tp[0]])   

    def calcpp(self, a, ta , k4, k5 ,k6 ,k7):
        
        res = [(ta-a) %256]
        res2 = []
        for r in res:
            for i in self.CVI.getinverse(r):
                res2.append((((i -k7 )^k6)-a) %256)
        
        res = []
        for r in res2:
            for i in self.CVI.getinverse(r):
                res.append(((((i)-k5)^k4)-a)%256)
        
        res2 = []  
        for r in res:
            for i in self.CVI.getinverse(r):
                res2.append(i)
        
        return res2

    def createHashTablesecond(self):
        self.temp = CMEA()
        for k4 in xrange(256):
            print k4
            for k5 in xrange(256):
                for (k6,k7) in self.possible67:
                    tpp = [self.calcpp(a,ta,k4,k5,k6,k7) for (a,ta) in self.tuples]
                    if [] in tpp:
                        continue
                    for (a,b,c,d) in [(a,b,c,d) for a in tpp[0] for b in tpp[1] for c in tpp[2] for d in tpp[3]]:
                        m = ((a-d)%256,(b-d)%256, (c-d)%256)
                        m = m[0]*256**2 + m[1]*256+m[2]
                        if m in self.startmap:
                            for k in self.startmap[m]:
                                key = k[:3]
                                key.append((a-k[3])%256)
                                key.extend([k4,k5,k6,k7])
                                if key[:3]==[1,2,3]:
                                    print key
                                if self.trialencryption(key):
                                    print "cle trouve: ",key
                                    return True
    
    def trialencryption(self, key):
        self.temp.setkey(key)
        good=True
        for (P,C) in self.texts:
            if not P==self.temp.crypt(C) or not C == self.temp.crypt(P)):
                good = False
                break
        return good
                    

class Parallel(Thread):
    def __init__(self, t, c, texts, d):
        Thread.__init__(self)
        self.c=c
        self.decrypt = d
        self.t=t
        self.texts=texts
        self.l=[]
    
    def run(self):
        print "demarre"
        for x in self.t:
            if(x in cavetable and self.decrypt.checkT0Value(x)):
                self.l.append(x)
                print x, " good"
            else:
                print x, "not good"
    
