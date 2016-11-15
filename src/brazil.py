#!/usr/bin/env python
# -*- coding: utf-8 -*-
from windows import *

fname = input("nome do arquivo: ")

x = []
y = []
segments = []

with open(fname) as f:
    lines = [line.rstrip('\n') for line in f]
    for l in lines:
        aux = l.split(' ')
        x1 = int(aux[0])
        x2 = int(aux[2])
        y1 = int(aux[1])
        y2 = int(aux[3])
        x.append(x1)
        x.append(x2)
        y.append(y1)
        x.append(y2)
        segments.append(Segment(Point(x1,y1),Point(x2,y2)))
        
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)

    print("min x: ",min_x,"max x: ",max_x)
    print("min y: ",min_y,"max y: ",max_y)

    alpha = max_x - min_x
    beta = max_y - min_y

    T = Window(segments)

    count = 0
    k = 8
    if fname != "brasil.in": k = 0
    for i in range(k):
        for j in range(k):
            fl = open("brazil/brazil"+str(count)+".out",'w+')
            A = Point(min_x+i*alpha/k,min_y+j*beta/k)
            B = Point(min_x+(i+1)*alpha/k,min_y+(j+1)*beta/k)
            resp = T.query((A,B))
            for r in resp:
                x1 = r.beg.x
                x2 = r.end.x
                y1 = r.beg.y
                y2 = r.end.y
            
                s = str(x1) + " " + str(y1) + "\n" + str(x2) + " " + str(y2)
                print(s,file=fl)

            fl.close()
            print(count)
            count+=1
