#!/usr/bin/python
#-*- coding:utf-8 -*-

import ThreeByte
d = ThreeByte.Cryptanalysis3B()
print "key : ", d.c.key
d.findT0()
d.getPossible67values()
d.get4tuples()
d.createHashTableprime()
d.createHashTablesecond()
print "real key : ", d.c.key
raw_input()