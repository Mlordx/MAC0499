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
        if len(v) == 0 : return
        for i in range(2*len(v)-1): p.append(0)

        h = ceil(log(len(v),2))
        l2 = pow(2,h) - len(v)
        l = int(len(v) - l2)
        i = 2*len(v)-2

        for j in range(l-1,-1,-1):
            p[i] = VerticalNode(v[j],i,i,True)
            i -= 1

        for j in range(len(v)-1,l-1,-1):
            p[i] = VerticalNode(v[j],i,i,True)
            i -= 1
            
        while i >= 0:
            p[i] = VerticalNode(p[p[2*i+1].pr].point,p[2*i+2].pr,p[2*i+1].pl)
            i -= 1

        return p

    def getLeaves(self,ind):
        return self.tree[self.tree[ind].pl:self.tree[ind].pr+1]
        
    def findDividingVerticalNode(self,segment):
        w1,w2 = segment
        ind = 0
        div = self.tree[ind]
        
        while (not div.leaf) and (w1.y > div.point.y or (w2.y < div.point.y or (w2.y == div.point.y and w2.x <= div.point.x))):
            if w2.y < div.point.y or (w2.y == div.point.y and w2.x <= div.point.x):
                ind = 2*ind+1
            else:
                ind = 2*ind+2
            div = self.tree[ind]
        return div,ind
                
    def oneDimQuery(self,rng):
        w1,w2 = rng
        div,ind = self.findDividingVerticalNode(rng)
        p = [] 
        
        if div.leaf:
            if (w1.y < div.point.y or (w1.y == div.point.y and w1.x <= div.point.x)) and (div.point.y < w2.y or (div.point.y == w2.y and div.point.x <= w2.x)):
                p.append(div.point)
        else:
            ind2 = 2*ind+1 #Caminhando na Subárvore esquerda
            v = self.tree[ind2]

            while not v.leaf:
                if w1.y < v.point.y or (w1.y == v.point.y and w1.x <= v.point.x):
                    for pnt in self.getLeaves(2*ind2+2): p.append(pnt.point)
                    ind2 = 2*ind2+1
                    v = self.tree[ind2]
                else:
                    ind2 = 2*ind2+2
                    v = self.tree[ind2]

            if (w1.y < v.point.y or (w1.y == v.point.y and w1.x <= v.point.x)) and (v.point.y < w2.y or (v.point.y == w2.y and v.point.x <= w2.x)):
                p.append(v.point)

            ind2 = 2*ind+2 #Andando na subárvore direita
            v = self.tree[ind2]

            while not v.leaf:
                if w2.y > v.point.y:
                    for pnt in self.getLeaves(2*ind2+1): p.append(pnt.point)

                    ind2 = 2*ind2+2
                    v = self.tree[ind2]
                else:
                    ind2 = 2*ind2+1
                    v = self.tree[ind2]

            if (w1.y < v.point.y or (w1.y == v.point.y and w1.x <= v.point.x)) and (v.point.y < w2.y or (v.point.y == w2.y and v.point.x <= w2.x)):
                p.append(v.point)
        return p
            
class LimitTree2D:
    def __init__(self,v):
        self.root = self.buildTree(sorted(v,key = lambda a: a.x),sorted(v,key = lambda a: a.y))

    def inRange(self,rng,p):
        w1,w2 = rng
        return ((w1.x < p.x or (w1.x == p.x and w1.y <= p.y)) and (p.x < w2.x or (p.x == w2.x and p.y <= w2.y)) and (w1.y < p.y or (w1.y == p.y and w1.x <= p.x) and (p.y < w2.y or (p.y == w2.y and p.x <= w2.x))))


    def buildTree(self,vx,vy):
        v = Node(None)
        v.tree = VerticalTree(vy)
        lx = vx[:len(vx)//2]
        rx = vx[len(vx)//2:]

        n = len(vx)

        ly = []
        ry = []
        
        for i in range(n):
            if vy[i].x < vx[n//2-1].x or (vy[i].x == vx[n//2-1].x and vy[i].y <= vx[n//2-1].y):
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
                if w1.x < v.point.x or (w1.x == v.point.x and w1.y <= v.point.y):
                    p += v.r.tree.oneDimQuery(rng)
                    v = v.l
                else:
                    v = v.r

            if self.inRange(rng,v.point): p.append(v.point)

            v = div.r

            while not v.isLeaf():
                if w2.x > v.point.x:
                    p += v.l.tree.oneDimQuery(rng)
                    v = v.r
                else:
                    v = v.l

            if self.inRange(rng,v.point): p.append(v.point)
                
        return p
    
