#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from fractionalcascading import *
from segmenttree2d import *
from primitives import *

class Window:
    def __init__(self,s):
        self.l = []
        self.r = []
        for seg in s:
            self.l.append(Point(seg.beg.x,seg.beg.y,seg))
            self.r.append(Point(seg.end.x,seg.end.y,seg))

        self.layer_l = LayerTree(self.l)
        self.layer_r = LayerTree(self.r)

        self.seg_v = SegmentTree2Dx(s)
        self.seg_h = SegmentTree2Dy(s)

        self.S1 = None
        self.S2 = None
        self.S3 = None
        self.S4 = None

    def removeDuplicates(self,l,r,s1,s2,s3):
        resp = []
        for seg in l:
            if seg in r:
                l.remove(seg)
        resp = l + r

        for seg in s1:
            if (seg in resp) or intersect(seg,self.S3):
                s1.remove(seg)
                
        for seg in s3:
            if seg in resp:
                s3.remove(seg)

        for seg in s2:
            if (seg in resp) or (not intersect(seg,self.S4)):
                s2.remove(seg)

        resp += s1 + s2 + s3
        return resp
        
    def query(self,rng):
        # rng = (a,b)(c,d)
        # a <= c
        # b <= d
        L = self.layer_l.query(rng)
        R = self.layer_r.query(rng)
        l = []
        r = []
        
        for p in L: l.append(p.seg)
        for p in R: r.append(p.seg)
        
        a = rng[0].x
        b = rng[0].y
        c = rng[1].x
        d = rng[1].y
        
        seg1 = Segment(Point(a,b),Point(a,d))
        seg2 = Segment(Point(a,d),Point(c,d))
        seg3 = Segment(Point(c,b),Point(c,d))
        seg4 = Segment(Point(a,b),Point(c,b))
        
        s1 = self.seg_v.query(seg1)
        s3 = self.seg_v.query(seg3)
        s2 = self.seg_h.query(seg2)

        
        return list(set(l+r+s1+s2+s3))
