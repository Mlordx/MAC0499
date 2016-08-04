#!/usr/bin/env python
# -*- coding: utf-8 -*-

from infinitewindow import *
from primitives import *
from math import *
import copy

class HorizontalIntervalNode:
    def __init__(self,p=None,l=None,r=None):
        self.point = p
        self.l = l
        self.r = r
        self.L1 = None
        self.L2 = None

class HorizontalIntervalTree:
    def __init__(self,s):
        self.root = self.buildTree(sorted(s,key = lambda a : a.beg))

    def buildTree(self,s):
        n = len(s)

        if n > 0:
            v = HorizontalIntervalNode()
            l = [] 
            r = []
            l1 = []
            l2 = []

            v.point = s[n//2].beg

            i = 0

            while i < n and s[i].beg <= v.point:
                if s[i].end < v.point:
                    l.append(s[i])
                else:
                    l1.append(s[i])
                    l2.append(s[i])
                i+=1

            while i < n:
                r.append(s[i])
                i+=1


            aux = []
            for lft in l1:
                aux.append(Point(lft.beg.x,lft.beg.y,lft))
                
            v.L1 = minPrioritySearchTree(aux)

            aux = []

            for lft in l2:
                aux.append(Point(lft.end.x,lft.end.y,lft))

            v.L2 = maxPrioritySearchTree(aux)

            v.l = self.buildTree(l)
            v.r = self.buildTree(r)

        else:
            v = None

        return v

    def query(self,seg):
        return self.query_r(self.root,seg)

    def query_r(self,v,seg):
        l = []
        w1 , w2 = seg
        x = w1.x
        y = w1.y
        y2 = w2.y

        if v is not None:
            if x > v.point.x:
                rng = (Point(x,y),Point(inf,y2))
                l = v.L2.query(rng)
                l += self.query_r(v.r,seg)
            else:
                rng = (Point(-inf,y),Point(x,y2))
                l = v.L1.query(rng)
                l += self.query_r(v.l,seg)

        return l
