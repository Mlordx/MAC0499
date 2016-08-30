#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tree import *
from dcel import *
from tri import *
from geocomp.common.polygon import Polygon
from geocomp.common import prim
from geocomp.common import control
from geocomp.common.segment import Segment
from geocomp.common.guiprim import *
from geocomp import config
from geocomp.common.point import Point

"""
Implementação do algoritmo de linha de varredura para triangulação de Lee e Preparata(Para depois usar no algoritmo de Hertel e Mehlhorn, mas por enquanto deixo aqui a implementação individual dele)
"""

def criaAresta(u,w):
    aresta = Aresta()
    aresta.setAresta(Segment(u,w))

    aresta2 = Aresta()
    aresta2.setAresta(Segment(w,u))
    aresta.setGemeo(aresta2)
    aresta2.setGemeo(aresta)

    return aresta


def maisEmBaixoQue(a,b): #checa se o Ponto a está mais baixo que o ponto b
    return (a.y < b.y) or (a.y==b.y and a.x > b.x)

def maisEmCimaQue(a,b): #checa se o Ponto a está mais em cima que o ponto b
    return (a.y > b.y) or (a.y == b.y and a.x < b.x)



def pontaParaBaixo(x,pontos):
    if(x[1] == 0): ant = len(pontos)-1
    else: ant = x[1] - 1
    
    if(x[1] == len(pontos)-1): prox = 0
    else: prox = x[1] + 1

    if(maisEmCimaQue(pontos[ant][0],x[0]) and maisEmCimaQue(pontos[prox][0],x[0])): return True
    else: return False

def pontaParaCima(x,pontos):
    if(x[1] == 0): ant = len(pontos)-1
    else: ant = x[1] - 1
    
    if(x[1] == len(pontos)-1): prox = 0
    else: prox = x[1] + 1

    if(maisEmBaixoQue(pontos[ant][0],x[0]) and maisEmBaixoQue(pontos[prox][0],x[0])): return True
    else: return False


def esquerdaEst(aresta,ponto):
    return left(aresta.getAresta().init[0],aresta.getAresta().to[0],ponto[0])

def esquerda(aresta,ponto):
    return left_on(aresta.getAresta().init[0],aresta.getAresta().to[0],ponto[0])

def entre(aresta1,aresta2,ponto):
    if(esquerda(aresta1,aresta2.getAresta().init) ):
        return esquerdaEst(aresta1,ponto) and not esquerdaEst(aresta2,ponto)
    else:
        return not ( esquerda(aresta2,ponto) and not esquerda(aresta1,ponto) )


 
def insereDiagonal(vertice1,vertice2,diagonal,faces):
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

            ### Como eu estava pegando o angulo entre 2 arestas incidindo nos vertices, aqui eu as inverto
            aux = adj2.getGemeo()
            adj2 = aux

            aux = adj4.getGemeo()
            adj4 = aux
            ###
            
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

            vertice2.setAresta(diagonal.getGemeo())
            vertice1.setAresta(diagonal)

            faces.append(face1)
            faces.append(face2)
            break            
        
        e = (e.getProx()).getGemeo()
        if(aux is None): aux = e
   



def trataCaso1(u,v,w,arvore,pontos,vertices,diagonais,faces):
    if(u.y < w.y or (u.y == w.y and u.x > w.x ) ): #u <=> w
        aux = w
        w = u 
        u = aux

    aux = (arvore.get(v[0])).trap #aux recebe um trapézio que contem v
    arvore.delete(v[0])
        
    if(v[0].x == aux[0].to.x and v[0].y == aux[0].to.y): 
        arvore.insert((Segment(v[0],w),v,aux[2]))
    else:
        arvore.insert((aux[0],v,Segment(v[0],w)))

    if(pontaParaBaixo(aux[1],pontos)):
        diagonais.append(Segment(aux[1][0],v[0]))

        aresta = criaAresta(aux[1],v)

        Segment(aux[1][0],v[0]).hilight("blue")
        control.sleep()
        insereDiagonal(vertices[aux[1][1]-1],vertices[v[1]-1],aresta,faces)

def trataCaso2(u,v,w,arvore,vertices,diagonais,faces):
    if(left(u,v[0],w )): # u<=>w
        aux = w
        w = u
        u = aux

    aux = arvore.get(v[0])
    arvore.delete(v[0])

    if(aux is None):
        arvore.insert( ( Segment(v[0],u),v,Segment(v[0],w) ) )
    else:
        trap = aux.trap
        arvore.insert( (Segment(v[0],w),v,trap[2]) )  #insiro esse primeiro para respeitar a ordem correta na arvore(dado que eu escolhi comparar por x do vertice de apoio
        arvore.insert( (trap[0],v,Segment(v[0],u)) )

        diagonais.append( Segment(trap[1][0],v[0]) )

        aresta = criaAresta(trap[1],v)
        
        Segment(trap[1][0],v[0]).hilight("blue")
        control.sleep()
        insereDiagonal(vertices[trap[1][1]-1],vertices[v[1]-1],aresta,faces)
        
def trataCaso3(v,arvore,pontos,vertices,diagonais,faces):
    aux = (arvore.get(v[0])).trap
    arvore.delete(v[0])

    if(pontaParaBaixo(aux[1],pontos)):#aux[1] = vertice de apoio do trapézio
        diagonais.append(Segment(aux[1][0],v[0]))

        aresta = criaAresta(aux[1],v)

        Segment(aux[1][0],v[0]).hilight("blue")
        control.sleep()
        insereDiagonal(vertices[aux[1][1]-1],vertices[v[1]-1],aresta,faces)

    
    if( ((aux[0].to.x != v[0].x and aux[0].to.y != v[0].y) or (aux[2].init.x != v[0].x and aux[2].init.y != v[0].y)) ):#caso tenham 2 trapézios com v 
        aux2 =  arvore.get(v[0]) #segundo trapexio que contem v
        if(aux2):
            aux2 = aux2.trap
            arvore.delete(v[0])

            if(pontaParaBaixo(aux2[1],pontos)): #aux2[1] = vertice de apoio do segundo trapézio
                diagonais.append(Segment(aux2[1][0],v[0]))

                aresta = criaAresta(aux2[1],v)

                Segment(aux2[1][0],v[0]).hilight("blue")            
                control.sleep()
                insereDiagonal(vertices[aux2[1][1]-1],vertices[v[1]-1],aresta,faces)

            if( aux[2].to.x == v[0].x and aux[2].to.y == v[0].y):
                arvore.insert( (aux[0],v,aux2[2]) )
            else:
                arvore.insert( (aux2[0],v,aux[2]) )


def lp(l):
    #na arvore, cada trapezio é uma tripla (Segmento,(ponto,indice),Segmento), sendo então trapezio[0] o segmento esquerdo, trapezio[2] o direito e trapezio[1] o vértice de apoio

    arvore = Arvore()

    for x in range(len(l)):
        if(x != len(l)-1): l[x].lineto(l[(x+1)],'red')
        else: l[x].lineto(l[0],'red')                                    
    
    N = len(l)
    pontos = [] #lista de pontos, juntamente com seus indices originais
    verticesOrdenados = [] #lista de pontos ordenada
    diagonais = [] #lista das diagonais que particionam o poligono em poligonos menores monótonos

    for i in range(N): pontos.append((l[i],i))
    verticesOrdenados = sorted(pontos,key=lambda x: (x[0].y,-x[0].x), reverse=True)	 

    verticesDCEL = []
    arestas = []
    arestas2 = []

    ### Essa parte monta a face externa na mão
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
    ###

    for a in range(N):
        v = Vertice(aresta=arestas2[a])
        verticesDCEL.append(v)          


    face = Face(arestas2[0])
    faces = []

    faces.append(face)

############## Esse pedaço verifica se o poligono passado já é estritamente monotono. Se for ele passa a lista de pontos para o algoritmo de triangulação de monótonos
    monotono = True
    for i in range(1,N-1):
        if(pontaParaBaixo(verticesOrdenados[i],pontos) or pontaParaCima(verticesOrdenados[i],pontos)):
            monotono = False

    if(monotono == True):
        triangulaMonotono(faces[0].listaFace())
        return 0;
################

    for k in range(0,N):
        verticesOrdenados[k][0].hilight("yellow")

        if(verticesOrdenados[k][1] == 0): ant = len(l)-1
        else: ant = verticesOrdenados[k][1]- 1

        if(verticesOrdenados[k][1] == len(l)-1): prox = 0
        else: prox = verticesOrdenados[k][1] + 1

        pontos[ant][0].hilight("cyan")
        pontos[prox][0].hilight("green")
        control.sleep()

        if( (maisEmBaixoQue(pontos[ant][0],verticesOrdenados[k][0]) and maisEmCimaQue(pontos[prox][0],verticesOrdenados[k][0])) or (maisEmBaixoQue(pontos[prox][0],verticesOrdenados[k][0]) and maisEmCimaQue(pontos[ant][0],verticesOrdenados[k][0])) ):#Caso 1: uma aresta acima e outra embaixo
            trataCaso1(pontos[ant][0],verticesOrdenados[k],pontos[prox][0],arvore,pontos,verticesDCEL,diagonais,faces)
        elif(maisEmBaixoQue(pontos[ant][0],verticesOrdenados[k][0])): # Caso 2: as duas arestas abaixo
            trataCaso2(pontos[ant][0],verticesOrdenados[k],pontos[prox][0],arvore,verticesDCEL,diagonais,faces)
        else: #Caso 3: as duas arestas em cima
            trataCaso3(verticesOrdenados[k],arvore,pontos,verticesDCEL,diagonais,faces)

        verticesOrdenados[k][0].hilight("red")
        pontos[ant][0].hilight("red")
        pontos[prox][0].hilight("red")

    
    for f in faces:
        if( f != face ): # se não for a face externa
            triangulaMonotono(f.listaFace())

    for d in diagonais:
        d.hilight('blue')
