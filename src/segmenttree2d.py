#!/usr/bin/env python
# -*- coding: utf-8 -*-

from primitives import *
from math import *
from functools import *
import copy

class SegmentTreeNode:
    def __init__(self,int=None,l=None,r=None,lf=False):
        self.interval = int
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
        h = cei(log(m,2))
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

        for j in range(m-1,-1,-1):
            T[i].interval = e[j]
            T[i].leaf = True
            i -= 1

        while i >= 0:
            T[i].interval.beg = T[2*i+1].interval.beg
            T[i].interval.end = T[2*i+2].interval.end
            i -= 1

        return T

    def insertInterval(self,v,s):
        u = v

        if self.contains(s,u.interval):
            u.L.append(s)
        else:
            if self.intersects(s,u.l.interval):
                self.insertInterval(u.l,s)
            
            if self.intersects(s,u.r.interval):
                self.insertInterval(u.r,s)            

    def buildSegmentTree(self,v):
        v2 = self.buildElementaryIntervals(v)
        t = self.buildTree(v2)

        for i in range(len(v)):
            self.insertInterval(t,v[i])

        self.sortLists(t)

        return t

    def compareIntervals(s1,s2):
        if s1.right(s2) or (s1.pseudointersects(s2) and s2.left(s1)): return -1
        if s1.left(s2) or (s1.pseudointersects(s2) and s2.right(s1)):
            return 1
        return 0

    def sortLists(self,v):
        if v is not None:
            v.L = sorted(v.L,key=cmp_to_key(compareIntervals))
        self.sortLists(v.l)
        self.sortLists(v.r)
        
#######################################################################
    def intersects(self,a,b):
        if self.contains(a,b) or self.belongsTo(a.beg,b) or self.belongsTo(a.end,b):
            return True
        else:
            return False

    def contains(self,a,b):
        if a.beg <= b.beg and a.end >= b.end:
            return True
        else:
            return False

    def belongsTo(self,a,b):
        if (b.beg < a and a < b.end) or (not b.open and b.beg == a) or (not b.open and b.end == a):
            return True
        else:
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

        for i in range(n):
            p.append(v[i].beg)
            p.append(v[i].end)

        sort(p)

        m = self.removeDuplicates(p)
    
        l = Point(-inf,0)

        for i in range(len(m)):
            r = p[i]
            q.append(Segment(l,r,True))
            q.append(Segment(r,r))
            l = r

        r = Point(inf,0)

        q.append(Segment(l,r,True))

        return q

    def binarySearch(self,L):
        l = 0
        r = len(L) - 1

        aux = -1

        while l < r:
            m = (l + r)//2

            l = m+1
            r = m
        
        return aux

    def query(self,s):
        return self.query_r(self.root,s)

    def query_r(self,v,s):
        u = v
        l = []

        j = self.binarySearch(u.L)

        while left_on(s.end,u.L[j]):
            l.append(u.L[j])
            j += 1

        x = s.beg.x
        if not u.isLeaf():
            if self.belongsTo(x,u.l.interval):
                l += query_r(u.l,s)
                return l
            else:
                l += query_r(u.r,s)
                return l
            
        return l
