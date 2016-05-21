#!/usr/bin/env python
# -*- coding: utf-8 -*-

from primitives import *
from math import *

class VerticalNode:
    def __init__(self,p,pr,pl,l=False):
        self.point = p # Ponto associado ao nó
        self.pr = pr # indice do maior filho direito da subarvore direita
        self.pl = pl # indice do menor filho da subarvore esquerda
        self.leaf = l # boolean que fala se o nó é uma folha
        
class VerticalTree:
    def __init__(self,v):
        self.tree = self.buildTree(v)

    def buildTree(self,v):
        # Curiosidade: Quando v é um filho direito, segue que pl = indice(pai) + 1
        p = []
        for i in range(2*len(v)-1): p.append(0)
        
        h = ceil(log(len(v)))
        l2 = pow(2,h) - len(v)
        l = len(v) - l2
        i = 2*len(v)-2
        
        for j in range(l-1,-1,-1):
            aux = VerticalNode(v[j],j,j,True)
            p[i] = aux
            i -= 1

        for j in range(n-1,l-1,-1):
            aux = VerticalNode(v[j],j,j,True)
            p[i] = aux
            i -= 1
            
        while i >= 0:
            aux = VerticalNode(p[p[2*i+1].pr],p[2*i+2].pr,p[2*i+1].pl)
            p[i] = aux
            i -= 1

        return p

    def getLeaves(self,ind):
        return self.tree[self.tree[ind].pl:self.tree[ind].pr]
        
    def findDividingVerticalNode(self,segment):
        w1,w2 = segment
        ind = 0
        div = self.tree[ind]
        
        while (not div.leaf) and (w1.y > div.point.y or w2.y <= div.point.y):
            if w2.y <= div.point.y:
                ind = 2*ind+1
            else:
                ind = 2*ind+2
            div = self.tree[ind]
        return div,ind
                
    def 1dQuery(self,rng):
        w1,w1 = rng
        div,ind = self.findDividingVerticalNode(rng)
        p = []
        
        if div.leaf:
            if w1.y <= div.point.y and div.point.y <= w2.y:
                p.append(div.point)
        else:
            ind2 = 2*ind+1
            v = self.tree[ind2]

            while not v.leaf:
                if w1.y <= v.point.y:
                    self.getLeaves(2*ind2+2,p)
                    ind2 = 2*ind2+1
                    v = self.tree[ind2]
                else:
                    ind2 = 2*ind2+2
                    v = self.tree[ind2]

            if w1.y <= v.point.y and v.point.y <= w2.y:
                p.append(v.point)

            ind2 = 2*ind + 2
            v = self.tree[ind2]

            while not v.leaf:
                if w2.y > v.point.y:
                    self.getLeaves(2*ind2+1,p)
                    ind2 = 2*ind2+2
                    v = self.tree[ind2]
                else:
                    ind2 = 2*ind2+1
                    v = self.tree[ind2]

            if w1.y <= v.point.y and v.point.y <= w2.y:
                p.append(v.point)
        return p
            
class LimitTree2D:
    def __init__(self,v):
        self.size = 0
        self.root = self.buildTree(sorted(v,key = lambda a: a.x),sorted(v,key = lambda a: a.y))
        self.tree = None

    def inRange(rng,p):
        w1,w2 = rng
        return (w1.x <= p.x and p.x <= w2.x) and (w1.y <= p.y and p.y <= w2.y)


    def buildTree(self,vx,vy):
        v = Node(None)
        v.tree = VerticalTree(vy)
        lx = vx[:len(vx)//2]
        rx = points[len(vx)//2:]

        n = len(vx)

        ly = []
        ry = []

        for i in range(n):
            if vy[i].x <= vx[n//2-1].x:
                ly.append(vy[i])
            else: ry.append(vy[i])

        v.point = vx[n//2-1]
        
        if len(vx) == 1:
            v.l = v.r = None
        else:
            v.l = self.buildTree(lx,ly)
            v.r = self.buildTree(rx,ry)

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
        p = []
        w1,w2 = rng
        div = self.findDividingNode(rng)

        if div.isLeaf():
            if self.inRange(rng,div.point):
                p.append(div.point)
        else:
            v = div.l

            while not v.isLeaf():
                if w1.x <= v.point.x:
                    p += v.r.tree.1dQuery(rng)
                    v = v.l
                else:
                    v = v.r

            if self.inRange(rng,v.point):
                p.append(v.point)

            v = div.r

            while not v.isLeaf():
                if w2.x > v.point.x:
                    p += v.l.tree.1dQuery(rng)
                    v = v.r
                else:
                    v = v.l

            if self.inRange(rng,v.point):
                p.append(v.point)
                
        return p
    
