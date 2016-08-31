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
import geocomp.common as alx



def main(l):

    segments = [Segment(Point(-2,-2),Point(2,2)),Segment(Point(-3,-3),Point(3,-3)),Segment(Point(-4,-1),Point(1,5)),Segment(Point(10,0),Point(10,10)),Segment(Point(-5,-4),Point(4,-4)),Segment(Point(-10,5),Point(-2,2))]

    x = alx.segment.Segment(alx.point.Point(0,-11),alx.point.Point(0,11))
    y = alx.segment.Segment(alx.point.Point(-11,0),alx.point.Point(11,0))

    x.hilight("white" )
    y.hilight("white")

    alx.point.Point(11,11).hilight("black")
    alx.point.Point(-11,-11).hilight("black")
    alx.point.Point(11,-11).hilight("black")
    alx.point.Point(-11,11).hilight("black")

    alx.control.sleep()
    
    for bla in segments:
        aux = alx.point.Point(bla.beg.x,bla.beg.y)
        #aux.hilight()
        aux2 = alx.point.Point(bla.end.x,bla.end.y)
        #aux2.hilight()
        aux.lineto(aux2,'red')
        alx.control.sleep(0.1)

    alx.control.sleep()
    
    t8 = Window(segments)

    target = (Point(-2,-2),Point(2,2))
    a = target[0].x
    b = target[0].y
    c = target[1].x
    d = target[1].y
        
    seg1 = alx.segment.Segment(alx.point.Point(a,b),alx.point.Point(a,d))
    seg2 = alx.segment.Segment(alx.point.Point(a,d),alx.point.Point(c,d))
    seg3 = alx.segment.Segment(alx.point.Point(c,b),alx.point.Point(c,d))
    seg4 = alx.segment.Segment(alx.point.Point(a,b),alx.point.Point(c,b))
    seg1.hilight()
    seg2.hilight()
    seg3.hilight()
    seg4.hilight()

    alx.control.sleep()

    t = SegmentTree2Dy(segments)
    resp = t8.query(target)
    
    for bla in resp:
        aux = alx.point.Point(bla.beg.x,bla.beg.y)
        aux2 = alx.point.Point(bla.end.x,bla.end.y)
        aux.lineto(aux2,'cyan')
        alx.control.sleep()


