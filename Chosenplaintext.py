#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CMEA import *

class Decrypter:
    def setCrypter(self, crypt):
        self.c=crypt
    
    def findTzero(self):
        s = set()
        for c in cavetable:
            s.add(c)
        possibility = set()
        for i in s:
            S = self.c.crypt([(1-i)%256 for k in range(self.c.blocksize)])
            if S[0] == (-i %256):
                possibility.add(i)
        
        for p in possibility:
            print p, (-i %256) in s, self.c.Tbox(0)
        
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
            guess = (C[0] + t0) % 256
            if(not (guess-j)%256 in cavetable and not (guess-j+1)%256 in cavetable):
                print "pas ",t0
                return []
            else:
                if (guess-j) %256 in cavetable:
                    T[j].append((guess-j) % 256)
                if ((guess^1-j)%256) in cavetable:
                    T[j].append((guess-j+1)%256)
        return T

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
    
        
    
