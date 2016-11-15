#!/usr/bin/env python
# -*- coding: utf-8 -*-

fname = input("nome do arquivo: ")

x = []
y = []

with open(fname) as f:
    lines = [line.rstrip('\n') for line in f]
    for l in lines:
        aux = l.split(' ')
        x1 = int(aux[0])
        y1 = int(aux[1])
        x.append(x1)
        y.append(y1)
        
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)

    print("min x: ",min_x,"max x: ",max_x)
    print("min y: ",min_y,"max y: ",max_y)
