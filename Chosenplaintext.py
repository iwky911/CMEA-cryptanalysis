#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CMEA import *

class Decrypter:
    """
    a class that encapsulate all decryption methods
    """
    def __init__(self):
        self.knowntext=[]
        self.constraints = []
        self.known={}
    
    def setCrypter(self, crypt):
        self.c=crypt
    
    def findTzero(self):
        """
        find all possible t0 values
        """
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
        """
        return all possibles output for Tbox compatible with the cave table
        if, for one i, all possible output for Tbox(i) are not compatible with the cave table, we don't have the real t0, return []
        """
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

    def getallconstraints(self, t0):
        """
        extract all constraints possible when T(0)=t0
        """
        for i in range(1,256):
            self.getconstraints(i, t0)
    
    def getconstraints(self, j, t0):
        """
        get all constraints related to the message used to get T(j)
        """
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
            # set the value for each known output of T
            self.known[z[i] ^ i] = (Pp[i-1]-C[i]) % 256
            z.append((z[i]+ Pp[i-1])%256)
            
        # add the constraint on T(j) and T(zi^(n-1))
        self.constraints.append((C[-1], tjm, j, z[-1] ^ (n-1)))
    
    def solveconstraints(self):
        """
        check all constraints to see if we can deduce a T output value
        """
        compteur = 0
        for (c, tj, j, z) in self.constraints:
            if j in self.known:
                # if T(j) is known, we can affect the value for T(zn-1^(n-1))
                if not z in self.known:
                    compteur+=1
                self.known[z] = (self.known[j] - c) %256
            else:
                if z in self.known:
                    # if T(zn-1^(n-1)) is known, we can affect the value for T(j)
                    if not j in self.known:
                        compteur+=1
                    self.known[j] = (c + self.known[z]) % 256
                else:
                    # if one of the value if knwon (because the cave table invalidate one of the option) we can deduce the other value
                    posj = [tj, tj+1]
                    posz = [(tj-c)%256 , (tj+1 -c )%256]
                    posj = [k for k in posj if (k-j) %256 in cavetable]
                    posz = [k for k in posz if (k-z) %256 in cavetable]
                    if len(posj)==1:
                        self.known[j] = posj[0]
                    if len(posz)==1:
                        self.known[z] = posz[0]
        
        return compteur
                    
    
if __name__ == '__main__':
    d = Decrypter()
    d.setCrypter(CMEA())
    d.c.blocksize = 3
    d.c.createRandomKey()
    possibilities= d.findTzero()
    print "number of possible values for t0:",len(possibilities)
    
    for p in possibilities:
        # checks if the value for t0 is correct
        t = d.findPossibleOthers(p)
        if t != []:
            break
    
    d.getallconstraints(t[0][0])
    for i in range(10):
        print "number of Tbox output known at iteration ", i, " :", len(d.known)
        d.solveconstraints()
