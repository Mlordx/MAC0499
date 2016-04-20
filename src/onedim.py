#!/usr/bin/env python
# -*- coding: utf-8 -*-

from primitives import *

class LimitTree:
    def __init__(self,v):
        self.size = 0
        self.root = self.buildTree(sorted(v,key = lambda k: k.x))

    
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

        while(not div.isLeaf() and (w1 > div.point or w2 <= div.point)):
            if w2 <= div.point:
                div = div.l
            else:
                div = div.r
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


    def query(self,rng):
        w1,w2 = rng
        div = self.findDividingNode(rng)
        p = []
        if div.isLeaf():
            if w1 <= div.point and div.point <= w2:
              print(bcolors.FAIL + "appended 1: " + str(v.point) + bcolors.ENDC)
              p.append(div.point)
        else:
            v = div.l
            while(not v.isLeaf()):
                if w1 <= v.point:
                    subtree = v.r.listSubTree()
                    print(bcolors.WARNING + "sub: " + str(subtree) + bcolors.ENDC)
                    
                    for pnt in subtree:
                        if w1 <= pnt and pnt <= w1:
                            p.append(pnt)
                    v = v.l
                else:
                    v = v.r
            if w1 <= v.point and v.point <= w2:
                p.append(v.point)
                print(bcolors.FAIL + "appended 2: " + str(v.point) + bcolors.ENDC)


            v = div
            while(not v.isLeaf()):
                if w2 > v.point:
                    subtree = v.l.listSubTree()
                    print(bcolors.WARNING + "sub: " + str(subtree) + bcolors.ENDC)
                    for pnt in subtree:
                        if w1 <= pnt and pnt <= w1:
                            p.append(pnt)
                    v = v.r
                else:
                    v = v.l
            if w1 <= v.point and v.point <= w2:
                p.append(v.point)
                print(bcolors.FAIL + "appended 3: " + str(v.point) + bcolors.ENDC)


        print(bcolors.OKBLUE + "bla: " + str(p) + bcolors.ENDC)
        return p
    
