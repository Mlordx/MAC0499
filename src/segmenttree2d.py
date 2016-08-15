#!/usr/bin/env python
# -*- coding: utf-8 -*-

from primitives import *
from math import *
from functools import *
import copy

class SegmentTreeNode:
    def __init__(self,l=None,r=None,lf=False):
        self.interval = Segment(Point(-inf,-inf),Point(inf,inf))
        self.l = l
        self.r = r
        self.L = []
        self.leaf = lf

    def isLeaf(self):
        return (self.l is None) and (self.r is None)

class SegmentTree2D:
    def __init__(self,s):
        self.root = self.buildSegmentTree(s)

    def buildTree(self,e):
        m = len(e)
        h = ceil(log(m,2))
        l2 = 2**h - m
        l = m - l2
        i = 2*m - 2
        T = []

        for k in range(2*m-1):
            T.append(0)
            T[k] = SegmentTreeNode()
        
        for j in range(l-1,-1,-1):
            T[i].interval = e[j]
            T[i].leaf = True
            i -= 1

        for j in range(m-1,l-1,-1):
            T[i].interval = e[j]
            T[i].leaf = True
            i -= 1

        while i >= 0:
            T[i].interval.beg = T[2*i+1].interval.beg
            T[i].interval.end = T[2*i+2].interval.end
            i -= 1

        for k in range(2*m-1):
            if(2*k+1 < 2*m -1): T[k].l = T[2*k+1]
            if(2*k +2 < 2*m-1): T[k].r = T[2*k+2]

        return T[0]

    def insertInterval(self,v,s):
        #print("\n\n")
        u = v
        
        if self.contains(s,u.interval):
            #print("appending",s,"in",u.interval.beg.x,"~",u.interval.end.x)
            u.L.append(s)
        else:
            if u.l and self.intersects(s,u.l.interval):
                #print("fui pra esquerda de",u.interval.beg.x,"~",u.interval.end.x)
                self.insertInterval(u.l,s)
            
            if u.r and self.intersects(s,u.r.interval):
                #print("fui pra direita de",u.interval.beg.x,"~",u.interval.end.x)
                self.insertInterval(u.r,s)            

    def buildSegmentTree(self,v):
        v2 = self.buildElementaryIntervals(v)
        t = self.buildTree(v2)

        for i in range(len(v)):
            self.insertInterval(t,v[i])

        self.sortLists(t)

        return t

    def compareIntervals(self,s1,s2):
        if s1.right(s2) or (s1.pseudointersects(s2) and s2.left(s1)): return -1
        if s1.left(s2) or (s1.pseudointersects(s2) and s2.right(s1)): return 1
        return 0

    def sortLists(self,v):
        if v is not None:
            v.L = sorted(v.L,key=cmp_to_key(self.compareIntervals))
        if(v.l is not None): self.sortLists(v.l)
        if(v.r is not None): self.sortLists(v.r)
        
#######################################################################
    def intersects(self,a,b):
        #print("---------------------------")
        if self.contains(a,b) or self.belongsTo(a.beg,b) or self.belongsTo(a.end,b):
            #print(a,"contains",b,"=",self.contains(a,b))
            #print(a.beg,"belongs to",b,"=",self.belongsTo(a.beg,b))
            #print(a.end,"belongs to",b,"=",self.belongsTo(a.end,b))
            #print(a," intersecta ",b,"? True")
            #print("---------------------------")
            return True
        else:
            #print(a," intersecta ",b,"? False")
            #print("---------------------------")            
            return False

    def contains(self,a,b):# A contains B
        if a.beg.x == -inf and a.end.x == inf: return False
        
        if a.beg.x <= b.beg.x and b.end.x <= a.end.x:
            #print("b:",b," contem a:",a,"?: True")
            return True
        else:
            #print("b:",b," contem a:",a,"?: False")
            return False

    def belongsTo(self,p,s):
        if (s.beg.x < p.x and p.x < s.end.x) or (not s.open and s.beg.x == p.x) or (not s.open and s.end.x == p.x):
            #print(p," esta em ",s,"? True")
            return True
        else:
            #print(p," esta em ",s,"? False")
            return False

    def removeDuplicates(self,l):
        seen = set()
        seen_add = seen.add
        return [x for x in l if not (x in seen or seen_add(x))]
#####################################################################

    def buildElementaryIntervals(self,v):
        p = []
        q = []
        n = len(v)

        M = -inf
        for i in range(n):
            p.append(v[i].beg)
            p.append(v[i].end)
            if(v[i].beg.x > M): M = v[i].beg.x
            if(v[i].end.x > M): M = v[i].end.x

        p = sorted(p)

        ### tirando duplicatas 
        p2 = []

        aux = []
        for i in range(M+1):
            aux.append(-1)

        for i in range(len(p)):
            if aux[p[i].x] == -1:
                p2.append(p[i])
                aux[p[i].x] = 1337

        #m = self.removeDuplicates(p)

        ################################
    
        l = Point(-inf,0)

        #p2 é p sem repetições de x, len(p2) <= len(p)
        
        #for i in range(len(m)):
        for i in range(len(p2)):
            r = p2[i]
            q.append(Segment(l,r,True))
            q.append(Segment(r,r))
            l = r

        r = Point(inf,0)

        q.append(Segment(l,r,True))

        return q

    def binarySearch(self,p,L):
        l = 0
        r = len(L) - 1
        
        aux = inf
        
        if len(L) == 1 and right_on(p,L[0]):
            return 0

        while l < r:
            m = (l + r)//2

            if left(p,L[m]):
                #print(p," está à esquerda de ",L[m])
                r = m
            elif right_on(p,L[m]):
                #print(p," está à direita de/em ",L[m])
                aux = m
                l = m+1
        
        return aux

    def printTree(self):
        q = Queue()
        q.put((self.root,0,None))
        
        while(not q.empty()):
         aux,level,prev = q.get()
         if prev is not None : print("(",aux.interval.beg.x,",",aux.interval.end.x,")",level,"(",prev.interval.beg.x,",",prev.interval.end.x,")")
         else: print(aux.interval,level,None)
         
         if aux.l is not None:
             q.put((aux.l,level+1,aux))
         if aux.r is not None:
             q.put((aux.r,level+1,aux))

        print("\n")
        return


    def query(self,s):
        return self.query_r(self.root,s)

    def query_r(self,v,s):
        u = v
        l = []

        #print("intervalo: ",u.interval)

        j = self.binarySearch(s.beg,u.L)
        
        while j < len(u.L) and left_on(s.end,u.L[j]):
            #print("Appended ",u.L[j])
            l.append(u.L[j])
            j += 1

        x = s.beg
        if not u.isLeaf():
            if self.belongsTo(x,u.l.interval):
                l += self.query_r(u.l,s)
                #return l
            #else:
            if self.belongsTo(x,u.r.interval):
                l += self.query_r(u.r,s)
                #return l
            
        return l
