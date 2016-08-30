#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from fractionalcascading import *
from segmenttree2d import *
from primitives import *
import geocomp.common as alx


class Window:
    def __init__(self,s):
        self.l = []
        self.r = []
        for seg in s:
            self.l.append(Point(seg.beg.x,seg.beg.y,seg))
            self.r.append(Point(seg.end.x,seg.end.y,seg))

        self.layer_l = LayerTree(self.l)
        self.layer_r = LayerTree(self.r)

        self.seg_v = SegmentTree2Dx([x for x in s])
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
        
        for p in L:
            l.append(p.seg)
            alx.segment.Segment(alx.point.Point(p.seg.beg.x,p.seg.beg.y),alx.point.Point(p.seg.end.x,p.seg.end.y)).hilight("blue")
            alx.control.sleep()
            
            
        for p in R:
            r.append(p.seg)
            alx.segment.Segment(alx.point.Point(p.seg.beg.x,p.seg.beg.y),alx.point.Point(p.seg.end.x,p.seg.end.y)).hilight("yellow")
            alx.control.sleep()

            
        a = rng[0].x
        b = rng[0].y
        c = rng[1].x
        d = rng[1].y
        
        seg1 = Segment(Point(a,b),Point(a,d))
        self.S1 = seg1
        
        seg2 = Segment(Point(a,d),Point(c,d))
        self.S2 = seg2
        
        seg3 = Segment(Point(c,b),Point(c,d))
        self.S3 = seg3
        
        seg4 = Segment(Point(a,b),Point(c,b))
        self.S4 = seg4
        
        s1 = self.seg_v.query(seg1)
        s3 = self.seg_v.query(seg3)
        s2 = self.seg_h.query(seg2)

        p = seg1
        alx.segment.Segment(alx.point.Point(p.beg.x,p.beg.y),alx.point.Point(p.end.x,p.end.y)).hilight("magenta")
        alx.control.sleep()
        alx.segment.Segment(alx.point.Point(p.beg.x,p.beg.y),alx.point.Point(p.end.x,p.end.y)).hilight("green")        
        alx.control.sleep()
        for p in s1:
            alx.segment.Segment(alx.point.Point(p.beg.x,p.beg.y),alx.point.Point(p.end.x,p.end.y)).hilight("magenta")
            alx.control.sleep()

        p = seg3
        alx.segment.Segment(alx.point.Point(p.beg.x,p.beg.y),alx.point.Point(p.end.x,p.end.y)).hilight("orange")
        alx.control.sleep()
        alx.segment.Segment(alx.point.Point(p.beg.x,p.beg.y),alx.point.Point(p.end.x,p.end.y)).hilight("green")
        alx.control.sleep()

        for p in s3:
            alx.segment.Segment(alx.point.Point(p.beg.x,p.beg.y),alx.point.Point(p.end.x,p.end.y)).hilight("orange")
            alx.control.sleep()

        p = seg2
        alx.segment.Segment(alx.point.Point(p.beg.x,p.beg.y),alx.point.Point(p.end.x,p.end.y)).hilight("light green")
        alx.control.sleep()
        alx.segment.Segment(alx.point.Point(p.beg.x,p.beg.y),alx.point.Point(p.end.x,p.end.y)).hilight("green")
        alx.control.sleep()

        
        for p in s2:
            alx.segment.Segment(alx.point.Point(p.beg.x,p.beg.y),alx.point.Point(p.end.x,p.end.y)).hilight("light green")
            alx.control.sleep()            

        """
        print(seg1,seg2,seg3,seg4)
        print("l:",l)
        print("r:",r)
        print("s1:",s1)
        print("s2:",s2)
        print("s3:",s3)
        """
        
        return list(set(l+r+s1+s2+s3))
