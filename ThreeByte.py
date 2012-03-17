#!/usr/bin/python
#-*- coding:utf-8 -*-

from CMEA import *
from threading import Thread
import random

def getY1Z1(x, P, C):
    return (P[0] + x) % 256, (C[0] + x) % 256
    
def checkValue(c, T0, p, P, C):
    y1, z1 = getY1Z1(T0, P, C)
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

    
 
def buildP(x):
    p = [ [ True for i in range(256) ] for j in range(256) ]
    for i in range(256):
        for j in range(256):
            if(not ((j-i) % 256) in cavetable):
                p[i][j] = False
    return p
            
def checkT0Value(c, x, texts):
    p = buildP(x)
    continuer = True
    while(continuer):
       # print "iter"
        continuer = False
        for (P, C) in texts:
          #  print [ len([k for k in t if k!=0]) for t in p]
            continuer = continuer or checkValue(c, x, p, P, C)
        for (C, P) in texts:
            continuer = continuer or checkValue(c, x, p, P, C)
        for i in range(256):
            if(not (True in p[i])):
                return False
    
    return True
    
def findT0():
    c = CMEA()
    texts = createPlaintexts(80, c)
    for x in range(256):
        if(x in cavetable and checkT0Value(c, x, texts)):
            print x, "good!"
        else:
            print x, " not good"
    #print checkT0Value(c, c.Tbox(0), texts)
  
def findT0parallel():
    c= CMEA()
    texts = createPlaintexts(80, c)
    n = 8
    threadlist = []
    for i in range(n):
        t = range(i*256/n, (i+1)*256/n)
        threadlist.append(Parallel(t,c,texts))
    
    for t in threadlist:
        t.start()
    
    sortie = []
    for t in threadlist:
        t.join()
        sortie.extend(t.l)
    
def createPlaintexts(n, c, size=3):
    r = random. Random()
    l = []
    c.createRandomKey()
    print "t0", c.Tbox(0)
    c.blocksize = size
    for i in range(n):
        P=[r.randint(0,256) for k in range(size)]
        #P = [45, 89, 23]
        l.append((P, c.crypt(P)))
    return l


class Parallel(Thread):
    def __init__(self, t, c, texts):
        Thread.__init__(self)
        self.c=c
        self.t=t
        self.texts=texts
        self.l=[]
    
    def run(self):
        print "demarre"
        for x in self.t:
            if(x in cavetable and checkT0Value(self.c, x, self.texts)):
                self.l.append(x)
                print x, " good"
            else:
                print x, "not good"
    
