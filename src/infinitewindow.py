#!/usr/bin/env python
# -*- coding: utf-8 -*-

from primitives import *
from math import *
import copy
import pdb

class minPrioritySearchNode:
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
        v = minPrioritySearchNode(None)

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
                
            if n != 1: v.point = vy[ceil((n-1)/2)+d-1]

            for i in range(1,n):
                if vx[i].y < v.point.y or (vx[i].y == v.point.y and (vx[i].x <= v.point.x)): lx.append(vx[i])
                else: rx.append(vx[i])

            v.l = self.buildTree(lx,ly)
            v.r = self.buildTree(rx,ry)
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

    def findDividingNode(self,rng):
        p = []
        w1,w2 = rng
        div = self.root
        
        while (not div.isLeaf()) and (not div.isSemiLeaf()) and (w1.y > div.point.y and w2.y < div.point.y or (w2.y == div.point.y and ( w2.x <= div.point.x))) :
            pdb.set_trace()
            if self.inRange(rng,div.pmin):
                p.append(div.pmin)
            if w2.y < div.point.y or ( w2.y == div.point.y and ( w2.x <= div.point.x )):
                div = div.l
                print(div.l,div.r)
            else:
                div = div.r
                print(div.l,div.r)

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

class maxPrioritySearchNode:
    def __init__(self,p,l=None,r=None,pm=None):
        self.point = p
        self.l = l
        self.r = r
        self.pmax = pm

    def isLeaf(self):
        return (self.l is None) and (self.r is None)

    def isSemiLeaf(self):
        return (self.l is None) and (self.r is not None)

class maxPrioritySearchTree:
    def __init__(self,v):
        self.root = self.buildTree(sorted(v,key = lambda a: a.x),sorted(v,key = lambda a: a.y))

    def buildTree(self,vx,vy):
        v = maxPrioritySearchNode(None)

        n = len(vx)
        

        if n > 0:
            ly = []
            lx = []
            ry = []
            rx = []
            d = 0

            v.pmax = vx[n-1]

            for i in range(ceil((n-1)/2)+d):
                if len(vy) > 0 and vy[i] != v.pmax: ly.append(vy[i])
                else: d+=1
                
            for i in range(ceil((n-1)/2)+d,n):            
                if len(vy) > 0 and vy[i] != v.pmax: ry.append(vy[i])

            if n != 1: v.point = vy[ceil((n-1)/2)+d-1]

            for i in range(1,n):
                if vx[i].y < v.point.y or (vx[i].y == v.point.y and (vx[i].x <= v.point.x)): lx.append(vx[i])
                else: rx.append(vx[i])

            v.l = self.buildTree(lx,ly)
            v.r = self.buildTree(rx,ry)
        else:
            v = None

        return v

    def inRange(self,rng,p):
        w1,w2 = rng
        return ((w1.x < p.x or (w1.x == p.x and w1.y <= p.y)) and (p.x < w2.x or (p.x == w2.x and p.y <= w2.y)) and (w1.y < p.y or (w1.y == p.y and w1.x <= p.x) and (p.y < w2.y or (p.y == w2.y and p.x <= w2.x))))

    def pointsMaxHeap(v,rng):
        p = []

        if v is not None:
            if self.inRange(rng,v.point):
                p.append(v.point)
                p += self.pointsMaxHeap(v.l,rng)
                p += self.pointsMaxHeap(v.r,rng)
        return p

        
    def printTree(self):
        q = Queue()
        q.put((self.root,0,None))
        
        while(not q.empty()):
         aux,level,prev = q.get()
         strg = str(aux.point) + " " + str(level)
         if prev is not None: strg += " " + str(prev.point)
         strg += " max = " + str(aux.pmax)
         print(strg)
         
         if aux.l is not None:
             q.put((aux.l,level+1,aux))
         if aux.r is not None:
             q.put((aux.r,level+1,aux))
             
        return


    def findDividingNode(self,rng):
        p = []
        w1,w2 = rng
        div = self.root

        while (not div.isLeaf()) and (not div.isSemiLeaf()) and w1.y > div.point.y and w2.y < div.point.y or (w2.y == div.point.y and ( w2.x <= div.point.x)) :
            print(div)
            if self.inRange(rng,div.pmax):
                p.append(div.pmax)
            if w2.y < div.point.y or ( w2.y == div.point.y and ( w2.x <= div.point.x )):
                div = div.l
            else:
                div = div.r
        return p, div

    def query(self,rng):
        self.printTree()
        w1,w2 = rng

        p,div = self.findDividingNode(rng)

        if not div.isLeaf() and not div.isSemiLeaf():
            if self.inRange(rng,div.pmax):
                p.append(div.pmax)

            u = div.l

            while not u.isLeaf() and not u.isSemiLeaf():
                if self.inRange(rng,u.pmax):
                    p.append(u.pmax)

                if w1.y < u.pmax.y or ( w1.y == u.pmax.y and (w1.x <= u.pmax.x)):
                    p += self.pointsMaxHeap(u.r,rng)
                    u = u.l
                else:
                    u = u.r

            if self.inRange(rng,u.pmax):
                p.append(u.pmax)

            if u.isSemiLeaf():
                if self.inRange(rng,u.r.pmax):
                    p.append(u.r.pmax)
                    
            #ai faz pra direita
            u = div.r

            while not u.isLeaf() and not u.isSemiLeaf():
                if self.inRange(rng,u.pmax):
                    p.append(u.pmax)

                if u.pmax.y < w2.y or ( u.pmax.y == w2.y and ( u.pmax.x <= w2.x )):
                    p += self.pointMaxHeap(u.l,rng)
                    u = u.r
                else:
                    u = u.l
                    
            if self.inRange(rng,u.pmax):
                p.append(u.pmax)

            if u.isSemiLeaf():
                if self.inRange(rng,u.r.pmax):
                    p.append(u.r.pmax)
                
        else:
            if self.inRange(rng,div.pmax):
                p.append(div.pmax)

            if div.isSemiLeaf():
                if self.inRange(rng,div.r.pmax):
                    p.append(div.r.pmax)
        
        return p
