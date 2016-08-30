#!/usr/bin/env python
# -*- coding: utf-8 -*-


from primitives import *
from math import *
import copy

class LayerNode:
    def __init__(self,p,pl=None,pr=None,il=None,ir=None,side=None,nxt=None):
        self.point = p
        self.pl = pl
        self.pr = pr
        self.nxt = nxt
        #self.il = il
        #self.ir = ir
        self.side = side

class LayerTree:
    def __init__(self,v):
        vy = []
        for y in sorted(v,key = lambda a: a.y): vy.append(LayerNode(y))
        
        self.root = self.buildTree(sorted(v,key = lambda a: a.x),vy)

    def buildTree(self,vx,vy):
        v = Node(None)
        lx = vx[:len(vx)//2]
        rx = vx[len(vx)//2:]

        n = len(vx)

        ly = []
        ry = []

        r = l = 0

        for i in range(n):
            if vy[i].point.x < vx[n//2-1].x or ((vy[i].point.x == vx[n//2-1].x) and vy[i].point.y <= vx[n//2-1].y):
                ly.append(LayerNode(vy[i].point))
            else:
                ry.append(LayerNode(vy[i].point))

        v.tree = self.createPointers(vy,ly,ry)
        v.point = vx[n//2-1]

        if n == 1:
            v.l = v.r = None
        else:
            for k in range(len(ly)-1):
                ly[k].nxt = ly[k+1]
                
            for k in range(len(ry)-1):
                ry[k].nxt = ry[k+1]
            
            v.l = self.buildTree(lx,ly)
            v.r = self.buildTree(rx,ry)

        return v

    def createPointers(self,v,l,r):
        il = 0
        ir = 0
        i = 0

        n = len(v)
        nl = len(l)
        nr = len(r)

        if n == 1:
            v[0].pl = v[0].pr = None
            return v

        while i < n:
            if il < nl:
                v[i].pl = l[il]
                #v[i].il = il
                l[il].side = False
            else:
                v[i].pl = None

            if ir < nr:
                v[i].pr = r[ir]
                #v[i].ir = ir
                r[ir].side = True
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
        a = w1.x < p.x or (w1.x == p.x and w1.y <= p.y)
        b = p.x < w2.x or (p.x == w2.x and p.y <= w2.y)
        c = w1.y < p.y or (w1.y == p.y and w1.x <= p.x)
        d = p.y < w2.y or (p.y == w2.y and p.x <= w2.x)
        return a and b and c and d

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
        print("x:",x)
        for p in points:
            print(p.point)
        while l < r:
            m = (l + r)//2
            current = points[m].point
            if current.y == x.y: return points[m]
            
            elif current.y < x.y:
                l = m+1
            elif current.y > x.y or ( current.y == x.y and current.x >= x.x):
                aux = points[m]
                r = m-1
            print(l,r)

        return aux

    def printTree(self):
        q = Queue()
        q.put((self.root,0,None))
        
        while(not q.empty()):
         aux,level,prev = q.get()
         print(aux.point,level,prev)
         print("Tree: ")
         for v in aux.tree:
             print("<> ",v.point)
             if(v.pl is not None): print("<<: ",v.pl.point)
             else: print("<<: None")
             if(v.pr is not None): print(">>: ",v.pr.point)
             else: print(">>: None")
             print()
         
         if aux.l is not None:
             q.put((aux.l,level+1,aux))
         if aux.r is not None:
             q.put((aux.r,level+1,aux))
             
        return
    
    def query(self,rng):
        p = []
        w1,w2 = rng
        print("w1,w2: ",w1, " ", w2)
        
        div = self.findDividingNode(rng)
        
        print("div: ",div)

        if div.isLeaf():
            if self.inRange(rng,div.point):
                p.append(div.point)
        else:
            div2 = self.binarySearch(div.tree,w1) #menor ponto em div.tree >=_y que w1            
            print("div2: ",div2.point)
            if div2 is not None:
                v = div.l
                v2 = div2.pl

                print("v :",v.point," v2: ",v2.point)
                
                while not v.isLeaf() and v2 is not None:
                    if w1.x < v.point.x or ( w1.x == v.point.x and w1.y <= v.point.y ):
                        u = v2.pr                        
                        #ind = v2.ir
                        
                        #print(u.point,ind,u.side)
                        #for c in v.tree: print("~~~",c.point)
                        while u.side and (u.point.y < w2.y or ( u.point.y == w2.y and u.point.x <= w2.x)):
                            print("appended: ",u.point)#," with ind: ",ind)
                            p.append(u.point)
                            '''
                            ind += 1
                            
                            if ind < len(v.tree):
                                u = v.tree[ind]
                                print(u.point,ind,u.side)
                            else:
                                break
                            '''
                            u = u.nxt
                            if u is None: break
                            
                        v = v.l
                        v2 = v2.pl
                    else:
                        v = v.r
                        v2 = v2.pr
                    
                if v2 is not None and self.inRange(rng,v.point):
                    print("appended: ",v.point)
                    p.append(v.point)
                
            if div2 is not None:
                v = div.r
                v2 = div2.pr

                while not v.isLeaf() and v2 is not None:
                    if w2.x > v.point.x or (w2.x == v.point.x and w2.y >= v.point.y): # se pa
                        u = v2.pl
                        #ind = v2.il

                        while not u.side and (u.point.y < w2.y or ( u.point.y == w2.y and u.point.x <= w2.x)):
                            print("appended:", u.point)#," with ind", ind)
                            p.append(u.point)
                            '''
                            ind += 1
                            if ind < len(v.tree):
                                u = v.tree[ind]
                            else:
                                break
                            '''
                            u = u.nxt
                            if u is None: break
                        v = v.r
                        v2 = v2.pr
                    else:
                        v = v.l
                        v2 = v2.pl

                if v2 is not None and self.inRange(rng,v.point):
                    print("appended: ",v.point)
                    p.append(v.point)
           
        return p
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
        
