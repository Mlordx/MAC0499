#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from onedim import *
from twodim import *
from fractionalcascading import *
from horizontalsegments import *
from infinitewindow import *
from segments1d import *
from segmenttree1d import *
from segmenttree2d import *
from primitives import *
from windows import *
import geocomp
import geocomp.common.segment as seg
import geocomp.common.point as pnt

target = None
construct = False
t = None
segs = None

def main(l):
    global t
    global construct
    segments = []
    
    for i in range(0,len(l)-1,2):
        p1 = Point(l[i].x,l[i].y)
        p2 = Point(l[i+1].x,l[i+1].y)
        segments.append(Segment(p1,p2))
        
    geocomp.common.control.sleep()

    for bla in segments:
        aux = pnt.Point(bla.beg.x,bla.beg.y)
        aux2 = pnt.Point(bla.end.x,bla.end.y)
        aux.lineto(aux2,'red')
        alx.control.sleep(0.1)

    geocomp.common.control.sleep()

    
    if target is None: return
    a = target[0].x
    b = target[0].y
    c = target[1].x
    d = target[1].y
        
    seg1 = seg.Segment(pnt.Point(a,b),pnt.Point(a,d))
    seg2 = seg.Segment(pnt.Point(a,d),pnt.Point(c,d))
    seg3 = seg.Segment(pnt.Point(c,b),pnt.Point(c,d))
    seg4 = seg.Segment(pnt.Point(a,b),pnt.Point(c,b))
    seg1.hilight()
    seg2.hilight()
    seg3.hilight()
    seg4.hilight()

    geocomp.common.control.sleep()

    if t is None:
        print('\033[91m' +"\nErro! A árvore não foi construída!" + '\033[0m')
        return
    
    resp = t.query(target)
    
    for bla in resp:
        aux = pnt.Point(bla.beg.x,bla.beg.y)
        aux2 = pnt.Point(bla.end.x,bla.end.y)
        aux.lineto(aux2,'cyan')
        geocomp.common.control.sleep()


def init(l):
    global t
    global construct
    segments = []

    construct = None

    for i in range(0,len(l)-1,2):
        p1 = Point(l[i].x,l[i].y)
        p2 = Point(l[i+1].x,l[i+1].y)
        segments.append(Segment(p1,p2))
        
    t = Window(segments)
    print('\033[92m'+"\n Árvore construída com sucesso!" + '\033[0m')



