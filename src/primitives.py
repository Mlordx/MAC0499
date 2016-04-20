#!/usr/bin/env python
# -*- coding: utf-8 -*-

from  queue import *
from math import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    BOLD = "\033[1m"
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"
        
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)

    def __neg__(self):
        return Point(-1*self.x,-1*self.y)

    def __sub__(self,other):
        return Point(self.x-other.x,self.y-other.y)

    def __gt__(self,other):
        if(self.x == other.x): return self.y > other.y
        return self.x > other.x

    def __lt__(self,other):
        if(self.x == other.x): return self.y < other.y
        return self.x < other.x

    def __ge__(self,other):
        if(self.x == other.x): return self.y >= other.y
        return self.x >= other.x

    def __le__(self,other):
        if(self.x == other.x): return self.y <= other.y
        return self.x <= other.x

class Segment:
    def __init__(self,beg,end):
        self.beg = beg
        self.end = end

    def __str__(self):
        return "("+str(self.beg)+","+str(self.end)+")"

    def __add__(self,other):
        return Segment(self.beg+other.beg,self.end+other.end)

    def __sub__(self,other):
        return Segment(self.beg-other.beg,self.end-other.end)

class Node:
    def __init__(self,p,l=None,r=None):
        '''
        p = point
        l = left node
        r = right node
        '''
        self.point = p
        self.l = l
        self.r = r

    def __str__(self):
        return str(self.point)

    def isLeaf(self):
        return (self.l is None and self.r is None)

    def listSubTree(self):
        l = []
        self.makeThreads(l)
        l.append(self.point)
        return l

    def makeThreads(self,l):
        if self.isLeaf():
            l.append(self.point)
        
        if self.l is not None: self.l.makeThreads(l)
        if self.r is not None: self.r.makeThreads(l)

