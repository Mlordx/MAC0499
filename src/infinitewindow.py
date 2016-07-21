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

            v.point = vy[ceil((n-1)/2)+d]

            for i in range(1,n):
                if vx[i] < v.point: lx.append(vx[i])
                else: rx.append(vx[i])

            v.l = buildTree(lx,ly)
            v.r = buildTree(rx,ry)
        else:
            v = None

        return v

    def query(self,rng):
        return
