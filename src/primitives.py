#!/usr/bin/env python
# -*- coding: utf-8 -*-

from  Queue import *

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)

    def __neg__(self):
        return Point(-1*self.x,-1*self.y)

    def __sub__(self,other):
        return Point(self.x-other.x,self.y-other.y)

class Segment:
    def __init__(self,beg,end):
        self.beg = beg
        self.end = end

    def __str__(self):
        return "("+str(self.beg)+","+str(self.end)+")"

    def __add__(self,other):
        return Segment(self.beg+other.beg,self.end+other.end)

    def __sub__(self,other):
        return Segment(self.beg-other.beg,self.end-other.end)

class Node:
    def __init__(self,p,l=None,r=None):
        self.point = p
        self.l = l
        self.r = r

    def __str__(self):
        return str(self.point)
    
class LimitTree:
    def __init__(self,l):
        self.size = 0
        self.points = sorted(l,key = lambda k: k.x)
        self.root = self.buildTree(l)

    
    def buildTree(self,points):
        v = Node(None)

        e = points[:len(points)/2]
        d = points[len(points)/2:]

        v.point = points[len(points)/2]

        if len(points) == 1:
            v.l = v.r = None
        else:
            v.l = self.buildTree(e)
            v.r = self.buildTree(d)

        return v
    
    def printTree(self):
        q = Queue()
        q.put(self.root)
        level = 0
        p = []

        for i in range(2*len(self.points)):
            p.append([])
        
        while(not q.empty()):
         aux = q.get()
         p[level].append(aux)
         level+=1
         
         if aux.l is not None:
             q.put(aux.l)
             p[level].append(aux.l)
         if aux.r is not None:
             q.put(aux.r)
             p[level].append(aux.l)

            
        for i in range(level):
            for j in range(len(p[i])):
                print(str(p[i][j])+ " ")
            print("\n")
        
        
        
