#!/usr/bin/env python
# -*- coding: utf-8 -*-


from primitives import *
from math import *
import copy

class LayerNode:
    def __init__(self,p,pl=None,pr=None,il=None,ir=None):
        self.point = p
        self.pl = pl
        self.pr = pr
        self.il = il
        self.ir = ir
        

class LayerTree:
    def __init__(self,v):
        vy = []
        for y in sorted(v,key = lambda a: a.y):
            vy.append(LayerNode(y))
        
        self.root = self.buildTree(sorted(v,key = lambda a: a.x),vy)

    def buildTree(self,vx,vy):
        v = Node(None)
        v.tree = vy
        lx = vx[:len(vx)//2]
        rx = vx[len(vx)//2:]

        n = len(vx)

        ly = []
        ry = []

        for i in range(n):
            if vy[i].point.x < vx[n//2-1].x or ((vy[i].point.x == vx[n//2-1].x) and vy[i].point.y <= vx[n//2-1].y):
                ly.append(vy[i])
            else: ry.append(vy[i])

        vy = self.createPointers(vy,ly,ry)
        v.point = vx[n//2-1]

        if n == 1:
            v.l = v.r = None
        else:
            ly2 = []
            for p in ly: ly2.append(LayerNode(p.point))

            ry2 = []
            for p in ry: ry2.append(LayerNode(p.point))

            v.l = self.buildTree(lx,ly2)
            v.r = self.buildTree(rx,ry2)

        return v

    def createPointers(self,v,l,r):
        il = 0
        ir = 0
        i = 0

        n = len(v)
        nl = len(l)
        nr = len(r)

        while i < n:
            if il < nl:
                v[i].pl = l[il]
                v[i].il = i
            else:
                v[i].pl = None

            if ir < nr:
                v[i].pr = r[ir]
                v[i].ir = i
            else:
                v[i].pr = None

            if il < nl and v[i].point == l[il].point:
                il += 1
            else:
                ir += 1

            i += 1

        return v

    def inRange(self,rng,p):
        w1,w2 = rng
        return ((w1.x < p.x or (w1.x == p.x and w1.y <= p.y)) and (p.x < w2.x or (p.x == w2.x and p.y <= w2.y)) and (w1.y < p.y or (w1.y == p.y and w1.x <= p.x) and (p.y < w2.y or (p.y == w2.y and p.x <= w2.x))))

    def findDividingNode(self,segment):
        w1,w2 = segment
        div = self.root

        while(not div.isLeaf() and (w1 > div.point or w2 <= div.point)):
            if w2 <= div.point:
                div = div.l
            else:
                div = div.r
        return div


    def binarySearch(self,points,x):
        l = 0
        r = len(points)-1
        
        aux = None
        while l < r :
            m = (l + r)//2
            current = points[m].point
            if current == x: return points[m]
            
            elif current.y < x.y:
                l = m+1
            elif current.y > x.y or ( current.y == x.y and current.x >= x.x):
                aux = points[m]
                r = m
        return aux

    '''
    def inTree(self,points,v):
        l = 0
        r = len(points)-1

        if v is None: return(False,None)
                
        while l < r :
            m = (l + r)//2
            
            if points[m].point == v.point:
                return (True,m)
            elif points[m].point.y < v.point.y or (points[m].point.y == v.point.y and points[m].point.x < v.point.x):
                l = m+1
            elif points[m].point.y > v.point.y or (points[m].point.y == v.point.y and points[m].point.x > v.point.x):
                r = m
                
        return (False,None)
    '''

    
    def query(self,rng):
        p = []
        w1,w2 = rng
        div = self.findDividingNode(rng)

        
        if div.isLeaf():
            if self.inRange(rng,div.point):
                p.append(div.point)
        else:
            div2 = self.binarySearch(div.tree,w1)
            if div2 is not None:
                v = div.l
                v2 = div2.pl
                
                while not v.isLeaf() and v2 is not None:
                    if w1.x < v.point.x or ( w1.x == v.point.x and w1.y <= v.point.y ):
                        u = v2.pr
                        
                        inTree = u is not None
                        ind = v2.ir
                        while inTree and (u.point.y < w2.y or ( u.point.y == w2.y and u.point.x <= w2.x)):
                            p.append(u.point)
                            ind += 1
                            if ind < len(v.r.tree):
                                u = v.r.tree[ind]
                                inTree = True
                            else:
                                inTree = False
                            
                        v = v.l
                        v2 = v2.pl
                    else:
                        v = v.r
                        v2 = v2.pr

                if v2 is not None and self.inRange(rng,v.point):
                    p.append(v.point)

            if div2 is not None:
                v = div.r
                v2 = div2.pr

                while not v.isLeaf() and v2 is not None:
                    if w2.x > v.point.x or (w2.x == v.point.x and w2.y >= v.point.y):
                        u = v2.pl
                        inTree = u is not None
                        ind = v2.il
                        while inTree and (u.point.y < w2.y or ( u.point.y == w2.y and u.point.x <= w2.x)):
                            p.append(u.point)
                            ind += 1
                            if ind < len(v.l.tree):
                                u = v.r.tree[ind]
                                inTree = True
                            else:
                                inTree = False
                            
                        v = v.r
                        v2 = v2.pr
                    else:
                        v = v.l
                        v2 = v2.pl

                if v2 is not None and self.inRange(rng,v.point):
                    p.append(v.point)
           
        return p
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
        
