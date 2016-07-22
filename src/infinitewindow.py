#!/usr/bin/env python
# -*- coding: utf-8 -*-

from primitives import *
from math import *
import copy

class prioritySearchNode:
    def __init__(self,p,l=None,r=None,pm=None):
        self.point = p
        self.l = l
        self.r = r
        self.pmin = pm

    def isLeaf(self):
        return (self.l is None) and (self.r is None)

    def isSemiLeaf(self):
        return (self.l is not None) and (self.r is None)

class minPrioritySearchTree:
    def __init__(self,v):
        self.root = self.buildTree(sorted(v,key = lambda a: a.x),sorted(v,key = lambda a: a.y))

    def buildTree(self,vx,vy):
        v = prioritySearchNode(None)

        n = len(vx)

        if n > 0:
            ly = []
            lx = []
            ry = []
            rx = []
            d = 0

            v.pmin = vx[0]

            for i in range(ceil((n-1)/2)+d):
                if vy[i] != v.pmin: ly.append(vy[i])
                else: d+=1
                
            for i in range(ceil((n-1)/2)+d,n):            
                if vy[i] != v.pmin: ry.append(vy[i])

            v.point = vy[ceil((n-1)/2)+d-1]

            for i in range(1,n):
                if vx[i].y < v.point.y or (vx[i].y == v.point.y and (vx[i].x <= v.point.x)): lx.append(vx[i])
                else: rx.append(vx[i])

            v.l = buildTree(lx,ly)
            v.r = buildTree(rx,ry)
        else:
            v = None

        return v

    def inRange(self,rng,p):
        w1,w2 = rng
        return ((w1.x < p.x or (w1.x == p.x and w1.y <= p.y)) and (p.x < w2.x or (p.x == w2.x and p.y <= w2.y)) and (w1.y < p.y or (w1.y == p.y and w1.x <= p.x) and (p.y < w2.y or (p.y == w2.y and p.x <= w2.x))))

    def pointsMinHeap(v,rng):
        p = []

        if v is not None:
            if self.inRange(rng,v.point):
                p.append(v.point)
                p += self.pointsMinHeap(v.l,rng)
                p += self.pointsMinHeap(v.r,rng)
        return p

    def findDividingNode(rng):
        p = []
        div = self.root

        while not div.isLeaf() and not div.isSemiLeaf() and w1.y > div.point.y and w2.y < div.point.y or (w2.y == div.point.y and ( w2.x <= div.point.x)) :
            if self.inRange(rng,div.pmin):
                p.append(div.pmin)
            if w2.y < div.point.y or ( w2.y == div.point.y and ( w2.x <= div.point.x )):
                div = div.l
            else:
                div = div.r
        return p, div

    def query(self,rng):
        w1,w2 = rng

        p,div = self.findDividingNode(rng)

        if not div.isLeaf() and not div.isSemiLeaf():
            if self.inRange(rng,div.pmin):
                p.append(div.pmin)

            u = div.l

            while not u.isLeaf() and not u.isSemiLeaf():
                if self.inRange(rng,u.pmin):
                    p.append(u.pmin)

                if w1.y < u.pmin.y or ( w1.y == u.pmin.y and (w1.x <= u.pmin.x)):
                    p += self.pointsMinHeap(u.r,rng)
                    u = u.l
                else:
                    u = u.r

            if self.inRange(rng,u.pmin):
                p.append(u.pmin)

            if u.isSemiLeaf():
                if self.inRange(rng,u.l.pmin):
                    p.append(u.l.pmin)
                    
            #ai faz pra direita
            u = div.r

            while not u.isLeaf() and not u.isSemiLeaf():
                if self.inRange(rng,u.pmin):
                    p.append(u.pmin)

                if u.pmin.y < w2.y or ( u.pmin.y == w2.y and ( u.pmin.x <= w2.x )):
                    p += self.pointMinHeap(u.l,rng)
                    u = u.r
                else:
                    u = u.l
                    
            if self.inRange(rng,u.pmin):
                p.append(u.pmin)

            if u.isSemiLeaf():
                if self.inRange(rng,u.l.pmin):
                    p.append(u.l.pmin)
                
        else:
            if self.inRange(rng,div.pmin):
                p.append(div.pmin)

            if div.isSemiLeaf():
                if self.inRange(rng,div.l.pmin):
                    p.append(div.l.pmin)
        
        return p
