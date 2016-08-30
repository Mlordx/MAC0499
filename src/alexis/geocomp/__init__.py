# -*- coding: utf-8 -*-
"""Algoritmos de Geometria Computacional

Sub-modulos:
- convexhull: algoritmos para o problema do Fecho Convexo bidimensional
- farthest:   algoritmos para encontrar o par de pontos mais distante

- common:     classes e operacoes usadas por diversos algoritmos
- gui:        implementacoes das operacoes graficas
"""

import convexhull
import farthest
import triangulation
import mindecomposition
import ors
from common.guicontrol import init_display
from common.guicontrol import config_canvas
from common.guicontrol import run_algorithm
from common.io import open_file
from common.prim import get_count
from common.prim import reset_count

children = (   ( 'convexhull', None, 'Fecho Convexo' ),
	       ( 'farthest',  None, 'Par Mais Distante' ),
	       ('triangulation', None, 'Triangulacao' ),
	       ('mindecomposition',None,'Decomposição Mínima' ),
               ('ors',None,'Consultas em Janelas')
)

__all__ = map (lambda p: p[0], children)
