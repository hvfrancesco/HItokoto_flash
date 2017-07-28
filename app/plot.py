# -*- coding: utf-8 -*- 

from chiplotle import *
from chiplotle.tools.plottertools import instantiate_virtual_plotter
import ttfquery
from ttfquery import describe
from ttfquery import glyph
from math import pi
import random
import os
import textwrap


class plotter_virtuale():
    def __init__(self):
        self.p = instantiate_virtual_plotter(type="HP7550A")
        self.p.margins.hard.draw_outline()

    def scrivi(self, testo):
       x = random.randrange(self.p.margins.soft.right)
       y = random.randrange(self.p.margins.soft.top)
       dx = 0
       linee = []
       for linea in textwrap.wrap(testo,40, replace_whitespace=False):
       #for linea in testo.split(os.linesep):
           linea = self.rimpiazza_accenti(linea)
           linea = linea.encode('latin1','replace')
           s = shapes.label(linea, 0.1, 0.2)
           transforms.rotate(s, pi/2)
           transforms.offset(s, (x+100*dx,y))
           dx += 1
           linee.append(s)
       blocco = shapes.group(linee)
       tr_x = blocco.top_right.x
       tr_y = blocco.top_right.y
       m_right = self.p.margins.soft.right
       m_top = self.p.margins.soft.top
       #print (m_right, m_top)
       if (tr_y > m_top):
           off = m_top-tr_y
           transforms.offset(blocco,(0,off))
       if (tr_x > m_right):
           off = m_right-tr_x
           transforms.offset(blocco,(off,0)) 
       self.p.write(blocco)

    def scrivi_linea(self, linea, x, y):
       s = shapes.label(linea.encode('latin1','replace'), 0.1, 0.2)
       transforms.rotate(s, pi/2)
       transforms.offset(s, (100*x+100,y))
       self.p.write(s)
       
    def rimpiazza_accenti(self, s):
		c = [(u'\xe0',"a'"),(u'\xe8',"e'"),(u'\xe9',"e'"),(u'\xec',"i'"),(u'\xf2',"o'"),(u'\xf9',"u'")]
		for i in c:
			s = s.replace(i[0],i[1])
		return s


    def mostra_foglio(self):
        io.view(self.p)
