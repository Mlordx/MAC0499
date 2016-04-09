#!/usr/bin/env python
# -*- coding: utf-8 -*-

from primitives import *

class LimitTree:
    def __init__(self,v):
        self.size = 0
        self.points = sorted(v,key = lambda k: k.x)
        self.root = self.buildTree(v)

    
    def buildTree(self,points):
        v = Node(None)
        l = points[:len(points)//2]
        r = points[len(points)//2:]

        v.point = points[len(points)//2]

        if len(points) == 1:
            v.l = v.r = None
        else:
            v.l = self.buildTree(l)
            v.r = self.buildTree(r)

        return v

    def findDividingNode(self,segment):
        w1,w2 = segment
        div = self.root

        while(not div.isLeaf() and (w1 > div.point or div.point <= w2)):
            if w2 <= div.point:
                div = div.point.l
            else:
                div = div.point.r
        return div
    
    def printTree(self):
        q = Queue()
        q.put((self.root,0,None))
        
        while(not q.empty()):
         aux,level,prev = q.get()
         print(aux,level,prev)
         
         if aux.l is not None:
             q.put((aux.l,level+1,aux))
         if aux.r is not None:
             q.put((aux.r,level+1,aux))
             
        return


    def query(rng):
        w1,w2 = rng
        div = self.findDividingNode(rng)
        p = []
        if div.isLeaf():
            if w1 >= div.point and div.point <= w2:
              p.append(div.point)
        else:
            v = div.l
            while(not v.isLeaf()):
                if w1 <= v.point:
                    aux = []
                    subtree = v.r.point.listSubTree(aux)
                    p += subtree
                    v = v.l
                else:
                    v = v.r
            if w1 <= v.point and v.point <= w2:
                p.append(v.point)

            v = div
            while(not v.isLeaf()):
                if w2 > v.point:
                    aux = []
                    subtree = v.l.point.listSubTree(aux)
                    p += subtree
                    v = v.r
                else:
                    v = v.l
            if w1 <= v.point and v.point <= w2:
                p.append(v.point)

        return p
    
