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

def main(l):

    segments = [Segment(Point(-2,-2),Point(2,2)),Segment(Point(-3,-3),Point(3,-3)),Segment(Point(-4,-1),Point(1,5)),Segment(Point(10,0),Point(10,10)),Segment(Point(-5,-4),Point(4,-4)),Segment(Point(-10,5),Point(-2,2))]

    x = seg.Segment(pnt.Point(0,-11),pnt.Point(0,11))
    y = seg.Segment(pnt.Point(-11,0),pnt.Point(11,0))

    x.hilight("white" )
    y.hilight("white")

    pnt.Point(11,11).hilight("black")
    pnt.Point(-11,-11).hilight("black")
    pnt.Point(11,-11).hilight("black")
    pnt.Point(-11,11).hilight("black")

    geocomp.common.control.sleep()
    
    for bla in segments:
        aux = pnt.Point(bla.beg.x,bla.beg.y)
        aux2 = pnt.Point(bla.end.x,bla.end.y)
        aux.lineto(aux2,'red')
        alx.control.sleep(0.1)

    geocomp.common.control.sleep()
    
    t8 = Window(segments)

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

    t = SegmentTree2Dy(segments)
    resp = t8.query(target)
    
    for bla in resp:
        aux = pnt.Point(bla.beg.x,bla.beg.y)
        aux2 = pnt.Point(bla.end.x,bla.end.y)
        aux.lineto(aux2,'cyan')
        geocomp.common.control.sleep()

