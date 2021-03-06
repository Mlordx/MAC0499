#!/usr/bin/env python
# -*- coding: utf-8 -*-

import control
from geocomp import config

class Segment:
	"Um segmento de reta"
	def __init__ (self, pto_from=None, pto_to=None):
		"Para criar, passe os dois pontos extremos"
		self.init = pto_from
		self.to = pto_to
	
	def __repr__ (self):
		"retorna uma string da forma [ ( x0 y0 );( x1 y1 ) ]"
		return '[ '+`self.init`+'; '+`self.to`+' ]'

	def hilight (self, color_line=config.COLOR_HI_SEGMENT,
			color_point=config.COLOR_HI_SEGMENT_POINT):
		"desenha o segmento de reta com destaque na tela"
		self.lid = self.init.lineto (self.to, color_line)
		#self.pid0 = self.init.hilight (color_point)
		#self.pid1 = self.to.hilight (color_point)
		return self.lid
	
	def plot (self, cor=config.COLOR_SEGMENT):
		"desenha o segmento de reta na tela"
		self.lid = self.init.lineto (self.to, cor)
		return self.lid
	
	def hide (self, id=None):
		"apaga o segmento de reta da tela"
		if id == None: id = self.lid
		control.plot_delete (id)
