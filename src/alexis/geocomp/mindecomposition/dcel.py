#!/usr/bin/env python
# -*- coding: utf-8 -*-


from geocomp.common.prim import *

class Aresta:
    def __init__(self): #iniciando 
        self.aresta = None
        self.gemeo = None
        self.prox = None
        self.ant = None

    def setAresta(self,aresta):
        self.aresta = aresta

    def setGemeo(self,gemeo):
        self.gemeo = gemeo

    def setProx(self,prox):
        self.prox = prox

    def setAnt(self,ant):
        self.ant  = ant

    def getAresta(self):
        return self.aresta

    def getGemeo(self):
        return self.gemeo

    def getProx(self):
        return self.prox

    def getAnt(self):
        return self.ant



class Vertice:
    def __init__(self,aresta):
        self.aresta = aresta

    def getAresta(self):
        return self.aresta

    def setAresta(self,aresta):
        self.aresta = aresta

class Face:
    def __init__(self,aresta):
        self.aresta = aresta

    def getAresta(self):
        return self.aresta

    def listaFace(self):
        lista = []
        lista.append(self.aresta.getAresta().to[0])
        e = self.aresta.getAnt()
        while(e.getAresta() != self.aresta.getAresta()):
            lista.append(e.getAresta().to[0])
            e = e.getAnt()

        return lista

    def tamFace(self):
        contador = 1
        e = self.aresta.getAnt()
        while(e.getAresta() != self.aresta.getAresta()):
            contador += 1
            e = e.getAnt()

        return contador
