#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from dcel import *
from geocomp.common.polygon import Polygon
from geocomp.common import prim
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.guiprim import *
from geocomp import config
from geocomp.common.point import Point
"""
Implementação do algoritmo de triangulação de polígonos monótonos(Para posteriormente ser usado com o algoritmo de Lee e Preparata, mas por enquanto deixo ele aqui
para ser usado sozinho no programa)
"""


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    BOLD = "\033[1m"
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def merge(pontos,lado):
    N = len(pontos)
    verticesOrdenados = []
    yMax = -20000000
    yMin = 2000000
    vMax = pontos[0]
    vMin = pontos[N-1]

    for i in range(N):
        if(pontos[i][0].y == yMax and pontos[i][0].x < vMax[0].x): vMax = pontos[i]
        if(pontos[i][0].y == yMin and pontos[i][0].x > vMin[0].x): vMin = pontos[i]
        if(pontos[i][0].y > yMax):
            vMax = pontos[i]
            yMax = vMax[0].y
        if(pontos[i][0].y < yMin):
            vMin = pontos[i]
            yMin = vMin[0].y
            
    if(vMax[1] != N-1):v = pontos[vMax[1]+1]
    else: v = pontos[0]
            
    if(vMax[1]!= 0): i = vMax[1]-1
    else: i = N-1

    if(vMax[1]!= N-1):j = vMax[1]+1
    else: j = 0

    lado[vMin[1]] = False

    if(vMax[1]!= 0): i = vMax[1]-1
    else: i = N-1

    if(vMax[1]!= N-1):j = vMax[1]+1
    else: j = 0            

    verticesOrdenados.append(vMax);
    while(len(verticesOrdenados) < N): #Merge
        if(pontos[j] == vMin):
            while(pontos[i] != vMin):
                verticesOrdenados.append(pontos[i])
                if(i!=0):i -= 1
                else: i = N-1
        elif(pontos[i] == vMin):
            while(pontos[j] != vMin):
                lado[pontos[j][1]] = False
                verticesOrdenados.append(pontos[j])
                if(j != N-1):j += 1
                else: j = 0

        if((pontos[j][0].y >= pontos[i][0].y)):
            lado[pontos[j][1]] = False
            verticesOrdenados.append(pontos[j])
            if(j != N-1): j+= 1
            else: j = 0
        else:
            verticesOrdenados.append(pontos[i])
            if(i!=0):i -= 1
            else: i = N-1

    return verticesOrdenados


def criaAresta(u,w):
    aresta = Aresta()
    aresta.setAresta(Segment(u,w))

    aresta2 = Aresta()
    aresta2.setAresta(Segment(w,u))
    aresta.setGemeo(aresta2)
    aresta2.setGemeo(aresta)

    return aresta                    

def esquerdaEst(aresta,ponto):
    return left(aresta.getAresta().init[0],aresta.getAresta().to[0],ponto[0])

def esquerda(aresta,ponto):
    return left_on(aresta.getAresta().init[0],aresta.getAresta().to[0],ponto[0])

def entre(aresta1,aresta2,ponto):
    if(esquerda(aresta1,aresta2.getAresta().init) ):
        return esquerdaEst(aresta1,ponto) and not esquerdaEst(aresta2,ponto)
    else:
        return not ( esquerda(aresta2,ponto) and not esquerda(aresta1,ponto) )

def checaDiagonal(vertice1,vertice2,diagonal):
    adj1 = diagonal.getProx()
    adj2 = diagonal.getGemeo().getAnt()

    adj3 = diagonal.getAnt()
    adj4 = diagonal.getGemeo().getProx()

    if( (not esquerda(adj1,adj2.getAresta().init)) and (not esquerda(adj4,adj3.getAresta().init)) ):
        Segment(diagonal.getAresta().init[0],diagonal.getAresta().to[0]).hilight("black")
        
        adj2.setProx(adj1)
        adj1.setAnt(adj2)
        
        adj3.setProx(adj4)
        adj4.setAnt(adj3)
        

        face = Face(adj1)

    else: Segment(diagonal.getAresta().init[0],diagonal.getAresta().to[0]).hilight("cyan")

 
def insere(vertice1,vertice2,diagonal,faces):
    e  = vertice2.getAresta().getGemeo() #vertice2 é o final da diagonal a->b
    e2 = vertice1.getAresta().getGemeo()
    aux = aux2 =  None

    faceOriginal = Face(e)
    faceOriginal2 = Face(e.getGemeo())
    numArestas = faceOriginal.tamFace()
    numArestas2 = faceOriginal2.tamFace()

    while( (e.getProx()).getGemeo() != aux ):
        resp = not entre(e,(e.getProx()).getGemeo(),diagonal.getAresta().init)
        if(resp):
            adj = e
            adj2 = e.getProx().getGemeo()
            v1 = vertice1.getAresta()


            ########## Procura a aresta e a proxima de v1 na face atual
            while( (e2.getProx()).getGemeo() != aux2 ):
                if( entre((e2.getProx()).getGemeo(),e2,diagonal.getAresta().to)):
                    adj3 = e2
                    adj4 = (e2.getProx()).getGemeo()
                e2 = (e2.getProx()).getGemeo()
                if(aux2 is None): aux2 = e2
            ##########

            aux = adj2.getGemeo()
            adj2 = aux

            aux = adj4.getGemeo()
            adj4 = aux
            
            adj3.setProx(diagonal)
            diagonal.setAnt(adj3)

            diagonal.setProx(adj2)
            adj2.setAnt(diagonal)
            
            adj.setProx(diagonal.getGemeo())
            diagonal.getGemeo().setAnt(adj)

            diagonal.getGemeo().setProx(adj4)
            adj4.setAnt(diagonal.getGemeo())
            

            face1 = Face(diagonal)
            face2 = Face(diagonal.getGemeo())

            if((face1.tamFace() + face2.tamFace() - 2) != numArestas and (face1.tamFace() + face2.tamFace() - 2) != numArestas2 ): print bcolors.WARNING,"OPA! Algo errado nas faces",bcolors.ENDC

            vertice2.setAresta(diagonal.getGemeo())
            vertice1.setAresta(diagonal)

            faces.append(face1)
            faces.append(face2)
            break            
        
        e = (e.getProx()).getGemeo()
        if(aux is None): aux = e



def triangulaMonotono(l):#Os pontos devem vir em ordem anti-horária
    pontos = [] #lista com os pontos,juntamente com seus indices
    verticesOrdenados = [] #lista com os pontos ordenados
    pilha = [] #pilha usada no algoritmo
    diagonais = [] #lista de diagonais da triangulação
    lado = []

    for x in range(len(l)):#desenha poligono
        if(x != len(l)-1): l[x].lineto(l[(x+1)],'red')
        else: l[x].lineto(l[0],'red')
                                        
    N = len(l)

    for i in range(N): 
        pontos.append((l[i],i)) #transforma cada ponto numa dupla (ponto,indice)
        lado.append(True)

#####################################

    verticesDCEL = []
    arestas = []
    arestas2 = []

    for a in range(N):
        if(a != N-1):
            ar = Aresta()
            ar.setAresta(Segment(pontos[a],pontos[a+1]))

            ar2 = Aresta()
            ar2.setAresta(Segment(pontos[a+1],pontos[a]))

            ar.setGemeo(ar2)
            ar2.setGemeo(ar)

            arestas.append(ar)
            arestas2.append(ar2)
            
        else:
            ar = Aresta()
            ar.setAresta(Segment(pontos[a],pontos[0]))

            ar2 = Aresta()
            ar2.setAresta(Segment(pontos[0],pontos[a]))

            ar.setGemeo(ar2)
            ar2.setGemeo(ar)

            arestas.append(ar)
            arestas2.append(ar2)

    for k in range(len(arestas)):
        if(k!= 0 and k!= len(arestas)-1):
            arestas[k].setProx(arestas[k+1])
            arestas[k].setAnt(arestas[k-1])

            arestas2[k].setProx(arestas2[k-1])
            arestas2[k].setAnt(arestas2[k+1])
        elif(k == 0):
            arestas[k].setProx(arestas[k+1])
            arestas[k].setAnt(arestas[len(arestas)-1])

            arestas2[k].setProx(arestas2[len(arestas)-1])
            arestas2[k].setAnt(arestas2[k+1])
        else:
            arestas[k].setProx(arestas[0])
            arestas[k].setAnt(arestas[k-1])

            arestas2[k].setProx(arestas2[k-1])
            arestas2[k].setAnt(arestas2[0])

    for a in range(N):
        bla = Vertice(aresta=arestas2[a])
        verticesDCEL.append(bla)          


    face = Face(arestas2[0])
    faces = []

    faces.append(face)



######################################
    verticesOrdenados = merge(pontos,lado)
######################################
    
    pilha.append(verticesOrdenados[0])
    pilha.append(verticesOrdenados[1])

    for i in range(2,N):
        t = len(pilha)
        verticesOrdenados[i][0].hilight("yellow")
        control.sleep()
        if(verticesOrdenados[i][1] == 0): ant = len(l)-1
        else: ant = verticesOrdenados[i][1]-1

        if(verticesOrdenados[i][1] == len(l)-1): prox = 0
        else: prox = verticesOrdenados[i][1]+1

        #aqui pilha[t-1][1] é o St e pilha[0][1] o S1, de acordo com os slides

   #Caso A ########################
        if((ant == pilha[t-1][1] and prox != pilha[0][1]) or (ant != pilha[0][1] and prox == pilha[t-1][1])): #adjacente a St mas nao a S1   
            if(lado[pilha[t-1][1]] == True):   
                while(t>1 and left_on(pilha[t-1][0],pilha[t-2][0],verticesOrdenados[i][0]) and not (pilha[t-1][0].y == pilha[t-2][0].y and verticesOrdenados[i][0].y == pilha[t-1][0].y )):                    
                    pilha.pop()
                    t -= 1
                    d = Segment(verticesOrdenados[i][0],pilha[t-1][0])
                    d.hilight("green")
                    control.sleep()
                    diagonalASerInserida = criaAresta(verticesOrdenados[i],pilha[t-1])
                    diagonais.append(diagonalASerInserida)
                    insere(verticesDCEL[verticesOrdenados[i][1]-1],verticesDCEL[pilha[t-1][1]-1],diagonalASerInserida,faces)
            elif(t>1):
                while(t>1 and right_on(pilha[t-1][0],pilha[t-2][0],verticesOrdenados[i][0])  and not (pilha[t-1][0].y == pilha[t-2][0].y and verticesOrdenados[i][0].y == pilha[t-1][0].y )):
                    pilha.pop()
                    t -= 1
                    d = Segment(verticesOrdenados[i][0],pilha[t-1][0])
                    d.hilight("green")
                    control.sleep()
                    diagonalASerInserida = criaAresta(verticesOrdenados[i],pilha[t-1])
                    diagonais.append(diagonalASerInserida)
                    insere(verticesDCEL[verticesOrdenados[i][1]-1],verticesDCEL[pilha[t-1][1]-1],diagonalASerInserida,faces)

                    
            pilha.append(verticesOrdenados[i])

   #Caso B ########################
        if((ant != pilha[t-1][1] and prox == pilha[0][1]) or (ant == pilha[0][1] and prox != pilha[t-1][1])): #adjacente a S1 mas nao a St
            aux = pilha[t-1]
            while(t>1):
                d = Segment(verticesOrdenados[i][0],pilha[t-1][0])
                d.hilight("green")
                control.sleep()
                diagonalASerInserida = criaAresta(verticesOrdenados[i],pilha[t-1])
                diagonais.append(diagonalASerInserida)
                insere(verticesDCEL[verticesOrdenados[i][1]-1],verticesDCEL[pilha[t-1][1]-1],diagonalASerInserida,faces)
                pilha.pop()
                t -= 1
            pilha.pop()
            pilha.append(aux)
            pilha.append(verticesOrdenados[i])
   #Caso C ########################
        if((ant == pilha[t-1][1] and prox == pilha[0][1]) or (ant == pilha[0][1] and prox == pilha[t-1][1])): #adjacente a St e S1
            pilha.pop()
            while(t>2):
                t -= 1
                d = Segment(verticesOrdenados[i][0],pilha[t-1][0])
                d.hilight("green")
                control.sleep()
                diagonalASerInserida = criaAresta(verticesOrdenados[i],pilha[t-1])
                diagonais.append(diagonalASerInserida)
                insere(verticesDCEL[verticesOrdenados[i][1]-1],verticesDCEL[pilha[t-1][1]-1],diagonalASerInserida,faces)
                pilha.pop()
        verticesOrdenados[i][0].hilight("red")
        
    for d in diagonais:
        checaDiagonal(verticesDCEL[d.getAresta().init[1] -1 ],verticesDCEL[d.getAresta().to[1] -1 ],d)

