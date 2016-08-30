#!/usr/bin/env python
# -*- coding: utf-8 -*-


from primitives import *
from onedim import *
import math
import copy

class IntervalNode:
    def __init__(self,p=None,l=None,r=None):
        self.point = p
        self.l = l
        self.r = r
        self.L1 = []
        self.L2 = []
        
class IntervalTree1D:
    def __init__(self,s):
        self.root = self.buildTree(sorted(s,key = lambda a: a.beg))

    def buildTree(self,s):
        n = len(s)
        if n > 0:
            v = IntervalNode()
            l = []
            r = []
            v.point = s[n//2].beg

            i = 0

            while i < n and s[i].beg <= v.point:
                if s[i].end < v.point:
                    l.append(s[i])
                else:
                    v.L1.append(s[i])
                    v.L2.append(s[i])
                i+=1

            v.L2 = sorted(v.L2,key = lambda a: a.end,reverse = True)
            
            while i < n:
                r.append(s[i])
                i+=1
                
            v.l = self.buildTree(l)
            v.r = self.buildTree(r)

        else:
            v = None

        return v
    
    def printTree(self):
        q = Queue()
        q.put((self.root,0,None))
        
        while(not q.empty()):
         aux,level,prev = q.get()
         strg = str(aux.point) + " " + str(level)
         if prev is not None: strg += " " + str(prev.point)
         print(strg)
         
         if aux.l is not None:
             q.put((aux.l,level+1,aux))
         if aux.r is not None:
             q.put((aux.r,level+1,aux))
             
        return


    def query(self,p):
        return self.query_r(self.root,p)


    def query_r(self,v,p):
        l = []

        if v is not None:
            if p > v.point:
                rng = (p,Point(math.inf,0))
                aux = []
                for seg in v.L2:
                    aux.append(Point(seg.end.x,seg.end.y,s=seg))
                t = LimitTree(aux)
                l = t.query(rng)
                l += self.query_r(v.r,p)
            else:
                rng = (Point(-math.inf,0),p)
                aux = []
                for seg in v.L1:
                    aux.append(Point(seg.beg.x,seg.beg.y,s=seg))
                t = LimitTree(aux)
                l = t.query(rng)
                l += self.query_r(v.l,p)
                
        return l
