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




def main():
    '''
    points = [Point(2,2),Point(2,3),Point(3,2),Point(3,3),Point(0,0),Point(2,5),Point(4,0),Point(0,4),Point(8,8),Point(5,5), Point(7,2)]
    
    t = LimitTree2D(points)
    t2 = LayerTree(points)
    rng = (Point(0,0),Point(4,4))
    print("Fractional Cascading: ",t2.query(rng))
    print("Range Tree: ",t.query(rng))

    points = [Point(2,0),Point(4,0)]

    print("\n\nInfinite windows test:")
    
    rng = (Point(-math.inf,0),Point(4,4))
    t3 = minPrioritySearchTree(points)

    print("Points on the infinite window: ",t3.query(rng))

    print("\n\n")

    target = Point(2,0)

    segments = [Segment(Point(1,0),Point(4,0)),Segment(Point(3,0),Point(5,0)),Segment(Point(2,0),Point(10,0))]

    t4 = IntervalTree1D(segments)
    s = t4.query(target)
    print("Segments with",target,"in common: ")
    for bla in s:
        print(bla.seg)

    print("\n\n")

    segments = [Segment(Point(1,0),Point(4,0)),Segment(Point(3,-1),Point(5,-1)),Segment(Point(2,1),Point(10,1))]

    t5 = HorizontalIntervalTree(segments)
    target = (Point(2,-1),Point(2,1))
    print("Segmentos cortados por",target,":")
    s = t5.query(target)
    for bla in s:
        print(bla.seg)

    print("\n\n")
    '''
    segments = [Segment(Point(-2,-2),Point(2,2)),Segment(Point(-3,-3),Point(3,-3)),Segment(Point(-4,0),Point(1,5)),Segment(Point(10,0),Point(10,10)),Segment(Point(-5,-4),Point(4,-4))]
    
    t6 = SegmentTree2Dx(segments)
    
    target = Segment(Point(10,5),Point(10,7))

    print("")
    print("Segmentos cortados por ", target , ":")
    #t6.printTree()
    s = t6.query(target)
    print(s)

    t7 = SegmentTree2Dy(segments)

    target = Segment(Point(10,-3),Point(20,-3))
    #t7.printTree()
    print("\nSegmentos cortados por ", target , ":")
    print(t7.query(target))
main()

