#!/usr/bin/env python
# -*- coding: utf-8 -*-

from primitives import *
from math import *
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

class SegmentTree1D:
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

        return t

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
    
    def query(self,p):
        return self.query_r(self.root,p)

    def query_r(self,v,p):
        u = v

        l = u.L

        if not u.isLeaf():
            if self.belongsTo(p,u.l.interval):
                l += self.query_r(u.l,p)
                return l
            else:
                l += self.query_r(u.r,p)
                return l

        return l
        
