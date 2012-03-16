#!/usr/bin/python
#-*- coding:utf8 -*-


import CMEA

class Plaintext3B:
    def __init__(self, texts):
        self.knowntexts=texts
    
    def createT0GuessTable(self):
        self.table = {}
        for i in range(256):
            if i in CMEA.cavetable:
                self.table[i]=[[] for p in range(256)]
                for k in range(256):
                    self.table[i][k] = [(True if (j-k) %256 in CMEA.cavetable else False) for j in range(256)]
    
    def getyz1(self, t0, P,C):
        return ((P[0]+t0) %256, (C[0]+t0) % 256 )
    
    def getimplications(self, y1,z1, P, C, t0, t2):
        """
            return the implication in the form:
            ((a,b),((t1,r),(t2,r2)))
        """
        implic = []
        y2 = (y1+P[1]+t2)%256
        pp1 = (P[1]+t2)%256
        implic.append((z1^1,(pp1-C[1])%256))
        pp0= (P[0] + t0) %256
        ppp0=(C[0] + t0) % 256
        pp2 = pp0^ppp0
        implic.append
        implic.append
        
        
