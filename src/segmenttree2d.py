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

class SegmentTree2Dx:
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
            T[i].interval.beg_open = T[2*i+1].interval.beg_open            
            T[i].interval.end = T[2*i+2].interval.end
            T[i].interval.end_open = T[2*i+2].interval.end_open
            i -= 1

        for k in range(2*m-1):
            if(2*k+1 < 2*m -1): T[k].l = T[2*k+1]
            if(2*k +2 < 2*m-1): T[k].r = T[2*k+2]

        return T[0]

    def insertInterval(self,v,s):
        u = v

        if contains(s,u.interval):
            u.L.append(s)
        else:
            if u.l and intersects(s,u.l.interval):
                self.insertInterval(u.l,s)
            
            if u.r and intersects(s,u.r.interval):
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
            q.append(Segment(l,r,True,True))
            q.append(Segment(r,r))
            l = r

        r = Point(inf,0)

        q.append(Segment(l,r,True,True))

        return q

    def inside(self,p,s):
        a = s.beg
        b = s.end

        if not collinear(p,s): return False
        
        if a.x != b.x:
            return ((a.x <= p.x and p.x <= b.x) or (b.x <= p.x and p.x <= a.x))
        else:
            return ((a.y <= p.y and p.y <= b.y) or (b.y <= p.y and p.y <= a.y))

    def binarySearch(self,p,L):
        l = 0
        r = len(L) - 1
        
        aux = inf
        
        if len(L) == 1:
            if (right(p,L[0]) or self.inside(p,L[0])):
                return 0
            else:
                return inf
        
        while l <= r:
            m = (l + r)//2

            if left(p,L[m]):
                l = m+1
            elif right_on(p,L[m]) or self.inside(p,L[m]):
                aux = m
                r = m-1
        
        return aux

    def printTree(self):
        q = Queue()
        q.put((self.root,0,None))
        
        while(not q.empty()):
         aux,level,prev = q.get()
         if prev is not None :
             aux2 = ""
             for i in range(level): aux2 += "   "
             if aux.interval.beg_open: aux2 += "("
             else: aux2 += "["
             aux2 += str(aux.interval.beg.x)
             aux2 += ","
             aux2 += str(aux.interval.end.x)
             if aux.interval.end_open: aux2 += ") "
             else: aux2 += "] "
             aux2 += " <-"

             if prev.interval.beg_open: aux2 += "("
             else: aux2 += "["
             aux2 += str(prev.interval.beg.x)
             aux2 += ","
             aux2 += str(prev.interval.end.x)
             if prev.interval.end_open: aux2 += ") "
             else: aux2 += "] "

             for seg in aux.L:
                 aux2 += str(seg) + " "
             
             print(aux2)
         else: print("(-inf,inf)")
         
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

        
        j = self.binarySearch(s.beg,u.L)
        
        while j < len(u.L) and (left(s.end,u.L[j]) or self.inside(s.end,u.L[j])):            
            l.append(u.L[j])
            j += 1

        x = s.beg
        if not u.isLeaf():
            if belongsTo(x,u.l.interval):
                l += self.query_r(u.l,s)
                return l
            else:
                l += self.query_r(u.r,s)
                return l
            
        return l

class SegmentTree2Dy:
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
            T[i].interval.beg_open = T[2*i+1].interval.beg_open            
            T[i].interval.end = T[2*i+2].interval.end
            T[i].interval.end_open = T[2*i+2].interval.end_open
            i -= 1

        for k in range(2*m-1):
            if(2*k+1 < 2*m -1): T[k].l = T[2*k+1]
            if(2*k +2 < 2*m-1): T[k].r = T[2*k+2]

        return T[0]

    def insertInterval(self,v,s):
        u = v

        '''
        aux = ""

        aux += str(s) + " "

        if u.interval.beg_open: aux+= "("
        else: aux+= "["

        aux+= str(u.interval.beg.y) + " " + str(u.interval.end.y)
        
        if u.interval.end_open: aux+= ")"
        else: aux+= "]"

        aux += " " + str(self.contains(s,u.interval))

        print(aux)
        '''
        
        if self.contains(s,u.interval):
            u.L.append(s)
        else:
            if u.l and self.intersects(s,u.l.interval):
                self.insertInterval(u.l,s)

            if u.r and self.intersects(s,u.r.interval):
                self.insertInterval(u.r,s)            

    def buildSegmentTree(self,v):
        v2 = self.buildElementaryIntervals(v)
        t = self.buildTree(v2)

        for i in range(len(v)):
            self.insertInterval(t,v[i])

        self.sortLists(t)

        return t

    def compareIntervals(self,s1,s2):
        if s1.right(s2) or (s1.pseudointersects(s2) and s2.left(s1)):
            return 1
        if s1.left(s2) or (s1.pseudointersects(s2) and s2.right(s1)):
            return -1
        return 0

    def sortLists(self,v):
        if v is not None:
            v.L = sorted(v.L,key=cmp_to_key(self.compareIntervals))
        if(v.l is not None): self.sortLists(v.l)
        if(v.r is not None): self.sortLists(v.r)
        
#######################################################################
    def intersects(self,a,b):
        if self.contains(a,b) or self.belongsTo(a.beg,b) or self.belongsTo(a.end,b):
            return True
        else:
            return False

    def contains(self,a,b):# A contains B
        if a.beg.y <= b.beg.y and a.end.y >= b.end.y:
            return True
        else:
            return False

    def belongsTo(self,p,s):
        if (s.beg.y < p.y and p.y < s.end.y) or (not s.beg_open and s.beg.y == p.y) or (not s.end_open and s.end.y == p.y):
            return True
        else:
            return False

#####################################################################

    def buildElementaryIntervals(self,v):
        p = []
        q = []
        n = len(v)

        M = -inf
        for i in range(n):
            p.append(v[i].beg)
            p.append(v[i].end)
            if(v[i].beg.y > M): M = v[i].beg.y
            if(v[i].end.y > M): M = v[i].end.y

        p = sorted(p,key = lambda a: a.y)

        ### tirando duplicatas 
        p2 = []

        aux = []
        for i in range(M+1): aux.append(-1)

        for i in range(len(p)):
            if aux[p[i].y] == -1:
                p2.append(p[i])
                aux[p[i].y] = 1337

        #m = self.removeDuplicates(p)

        ################################
    
        l = Point(0,-inf)

        #p2 é p sem repetições de x, len(p2) <= len(p)
        
        #for i in range(len(m)):
        for i in range(len(p2)):
            r = p2[i]
            q.append(Segment(l,r,True,True))
            q.append(Segment(r,r))
            l = r

        r = Point(0,inf)

        q.append(Segment(l,r,True,True))

        return q

    def inside(self,p,s):
        a = s.beg
        b = s.end

        if not collinear(p,s): return False
        
        if a.x != b.x:
            return ((a.x <= p.x and p.x <= b.x) or (b.x <= p.x and p.x <= a.x))
        else:
            return ((a.y <= p.y and p.y <= b.y) or (b.y <= p.y and p.y <= a.y))

    def binarySearch(self,p,L):
        l = 0
        r = len(L) - 1
        
        aux = inf
        
        if len(L) == 1:
            if (left(p,L[0]) or self.inside(p,L[0])):
                return 0
            else:
                return inf
        
        while l <= r:
            m = (l + r)//2

            if right(p,L[m]):
                l = m+1
            elif left_on(p,L[m]) or self.inside(p,L[m]):
                aux = m
                r = m-1
        
        return aux

    def printTree(self):
        q = Queue()
        q.put((self.root,0,None))
        
        while(not q.empty()):
         aux,level,prev = q.get()
         if prev is not None :
             aux2 = ""
             for i in range(level): aux2 += "   "
             if aux.interval.beg_open: aux2 += "("
             else: aux2 += "["
             aux2 += str(aux.interval.beg.y)
             aux2 += ","
             aux2 += str(aux.interval.end.y)
             if aux.interval.end_open: aux2 += ") "
             else: aux2 += "] "
             aux2 += " <-"

             if prev.interval.beg_open: aux2 += "("
             else: aux2 += "["
             aux2 += str(prev.interval.beg.y)
             aux2 += ","
             aux2 += str(prev.interval.end.y)
             if prev.interval.end_open: aux2 += ") "
             else: aux2 += "] "

             for seg in aux.L:
                 aux2 += str(seg) + " "
             
             print(aux2)
         else: print("(-inf,inf)")
         
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

        j = self.binarySearch(s.beg,u.L)

        while j < len(u.L) and (right(s.end,u.L[j]) or self.inside(s.end,u.L[j])):            
            l.append(u.L[j])
            j += 1

        y = s.end
        if not u.isLeaf():
            if self.belongsTo(y,u.l.interval):
                l += self.query_r(u.l,s)
                return l
            else:
                l += self.query_r(u.r,s)
                return l
            
        return l
