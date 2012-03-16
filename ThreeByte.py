#!/usr/bin/python
#-*- coding:utf-8 -*-

from CMEA import *
import random

def getY1Z1(x, P, C):
    return (P[0] + x) % 256, (C[0] + x) % 256
    
def checkValue(T0, p, P, C):
    y1, z1 = getY1Z1(T0, P, C)
    change = False
    for guess in range(256):
        if(p[y1 ^ 1] == 1):
            #T(y1 ^ 1) = guess
            Pp1 = (P[1] + guess) % 256
            #P'(1) == P'(n-2)
            Ppp1 = (Pp1 ^ (Pp1 | 1)) % 256
            #Tz1 -> T(z1 ^ 1)
            Tz1 = (Ppp1 - C[1]) % 256
            y2 = (y1 + Pp1) % 256
            z2 = (z1 + Ppp1) % 256
            #P'2 avec ambiguité sur le LSB
            Pp0 = (P[0] + x) % 256
            Pp2 = (Pp0 ^ (C[0] + T0)) % 256
            #C[0] + T0 = Ppp0
            
            #T(y2 ^ 2) sauf LSB
            Ty2 = (Pp2 - P[2]) % 256
            Ppp2 = (Pp2 ^ (Pp0 | 1) % 256)
            
            #T(z2 ^ 2) sauf LSB
            Tz2 = (Pp2 - C[2]) % 256
            
            if(p[z1 ^ 1][Tz1] == 0):
                p[y1 ^ 1] = 0
                change = True
            if((p[y2 ^ 2][Ty2] == 0) and (p[y2 ^ 2][Ty2 ^ 1] == 0)):
                p[y1 ^ 1] = 0
                change = True
            if((p[z2 ^ 2][Tz2] == 0) and (p[z2 ^ 2][Tz2 ^ 1] == 0)):
                p[y1 ^ 1] = 0
                change = True
                
    return change

    
 
def buildP(x):
    p = [ [ 1 for i in range(256) ] for j in range(256) ]
    for i in range(256):
        for j in range(256):
            if(not j -i in cavetable):
                p[i][j] = 0
    return p
            
def checkT0Value(x, texts):
    p = buildP(x)
    continuer = true
    while(continuer):
        continuer = false
        for (P, C) in texts:
            continuer = continuer or checkValue(x, p, P, C)
    for i in range(256):
        if(not 1 in p[i]):
            return false
    
    return true
    
def findT0(texts):
    for x in range(256):
        if(checkT0Value):
            print x
    
def createPlaintexts(n, size=3):
    r = random.Random()
    l = []
    c = CMEA()
    c.blocksize = size
    for i in range(n):
        P=[r.randint(0,256) for k in range(size)]
        l.append((P, c.crypt(P)))
    return l
