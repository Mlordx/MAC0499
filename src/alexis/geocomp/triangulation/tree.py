#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geocomp.common.prim import *

"""
Implementação de árvore de busca binária para uso no algoritmo de linha de varredura de Lee e Preparata.
"""

class Node:
    def __init__(self,trap,left=None,right=None,parent=None):
        self.trap = trap #trapezio contido naquela folha
        self.l = left #nó esquerdo
        self.r = right #nó direito
        self.parent = parent #nó pai

    def replace(self,key,lc,rc): #substitui folha
        self.trap = key
        self.l = lc
        self.r = rc

        if(self.l is not None):
            self.l.parent = self
        if(self.r is not None):
            self.r.parent = self
    
    def __repr__(self, level=0):
        ret = "\t"*level+repr(self.trap)+"\n"
        if(self.l):ret += self.l.__repr__(level+1)
        else: ret += "\t"*(level+1)+"Esquerda Vazia\n"
        if(self.r):ret += self.r.__repr__(level+1)
        else: ret += "\t"*(level+1)+"Direita Vazia\n"
        return ret

class Arvore:
    def __init__(self):
        self.size = 0
        self.raiz = Node(None)

    def length(self): #função que devolve o tamanho
        return self.size

    def __len__(self): #overload no operador de tamanho
        return self.size

    def insert(self,x): #caso já haja raiz insere na árvore por recursão, senão apenas coloca o trapézio novo como raiz
        if(self.size > 0):
            self._insert(x,self.raiz)
        else:
            self.raiz = Node(x)
        self.size += 1

    def _insert(self,x,v):
        if(x[1][0].x <= v.trap[1][0].x):
            if(v.l is None):
                v.l = Node(x,parent=v)
            else:
                self._insert(x,v.l)
        else:
            if(v.r is None):
                v.r = Node(x,parent=v)
            else:
                self._insert(x,v.r)
        

    def contains(self,v,trap): #Checa se o trapézio do nó atual da árvore contém o ponto x
        if( (trap[0].init.x == v.x and trap[0].init.y == v.y) or (trap[0].to.x == v.x and trap[0].to.y == v.y) or (trap[2].init.x == v.x and trap[2].init.y == v.y) or (trap[2].to.x == v.x and trap[2].to.y == v.y)): 
            return True #caso ele esteja nas pontas de uma das arestas do trapézio
        elif(v.x == trap[1][0].x and v.y == trap[1][0].y): 
            return True #caso ele seja o vértice de apoio
        elif(left_on(trap[0].init,trap[0].to,v) and right_on(trap[2].init,trap[2].to,v) and  right_on(trap[0].init,trap[2].to,v) and left_on(trap[0].to,trap[2].to,v)): 
            return True
        else:
            return False #caso não esteja no trapézio

    def get(self,x):#acha primeiro trapezio na árvore que contém o vértice x
        if(self.size == 0): return None
        else:
            res = self._get(x,self.raiz)
            return res

    def _get(self,x,v):
        if(v is None):
            return v
        if(self.contains(x,v.trap)):
            return v

        if(x.x <= v.trap[1][0].x):
            return self._get(x,v.l)
        else:
            return self._get(x,v.r)

    def delete(self,x): #remove o primeiro trapézio encontrado com o Ponto x contido nele
        if(self.size > 1):
            r = self.get(x)
            if(r is not None):
                self.remove(r)
                self.size -= 1
        elif(self.size == 1 and self.contains(x,self.raiz.trap)): #caso o trapézio a ser removido fosse o único na árvore
            self.raiz = None
            self.size -= 1        

    def __delitem__(self,x):
        self.delete(x)

    def getMin(self): #acha o menor elemento da árvore
        x = self.raiz
        while(x.l):
            x = x.l
        return x

    def findSuccessor(self,hue): #acha o elemento que melhor substituiria o elemento retirado na arvore
        s = None
        if(hue.r):
            s = self.getMin()
        else:
            hue.parent.r = None
            s = hue.parent.findSuccessor()
            hue.parent.r = hue
        return s

    def spliceOut(self,x): #retira diretamente sem precisar de recursão
        if(not(x.l or x.r)):
            if(x.parent.l == x):
                x.parent.l = None
            else:
                x.parent.r = None
        elif(x.l or x.r):
            if(x.parent and x.parent.l == x):
                x.parent.l = x.l
            else:
                x.parent.r = x.l
                x.l.parent = x.parent
        else:
            if(x.parent and x.parent.l == x):
                x.parent.l = x.r
            else:
                x.parent.r = x.r
                x.r.parent = x.parent

    def remove(self,x):
        if(not(x.l or x.r)): #x é folha
            if(x == x.parent.l):
                x.parent.l = None
            else:
                x.parent.r = None
        elif(x.l and x.r): #x tem os dois filhos
            s = self.findSuccessor(x)
            x.trap = s.trap
            self.remove(s)
        else:
            if(x.l is not None):
                if(x.parent and x == x.parent.l): #é filho esquerdo
                    x.l.parent = x.parent
                    x.parent.l = x.l
                elif(x.parent and x == x.parent.r): #é filho direito
                    x.r.parent = x.parent
                    x.parent.r = x.r
                else: #x era a raiz
                    x.replace(x.l.trap,x.l.l,x.l.r)
            else:
                if(x.parent and x == x.parent.l): #é filho esquerdo
                    x.r.parent = x.parent
                    x.parent.l = x.r
                elif(x.parent and x == x.parent.r): #é filho direito
                    x.r.parent = x.parent
                    x.parent.r = x.r
                else:
                    x.replace(x.r.trap,x.r.l,x.r.r)


    def __repr__(self):
        return self.raiz.__repr__()
