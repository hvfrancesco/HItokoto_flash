# -*- coding: utf-8 -*- 

from chiplotle import *
from chiplotle.tools.plottertools import instantiate_virtual_plotter
from chiplotle.geometry.core.coordinate import Coordinate
import ttfquery
from ttfquery import describe
from ttfquery import glyph
from math import pi
import random
import os
import textwrap
import time


class plotter():
    def __init__(self):
        self.dim_foglio = Coordinate(33640,23760) # A1 - temporaneo
        self.p = instantiate_virtual_plotter(right_top = self.dim_foglio, type="HP7576A")
        # self.p = instantiate_plotters( )[0] # plotter reale
        self.p.margins.hard.draw_outline() # da rimuovere con plotter reale
        self.dimensioni_carattere = 0.3
        self.altezza_carattere = self.dimensioni_carattere*2
        self.fattore_interlinea = 1.4
        self.interlinea = self.altezza_carattere*400*self.fattore_interlinea
        self.n_caratteri = 40
        self.w_colonna = self.dimensioni_carattere*self.n_caratteri*400*1.6
        self.titolo = "HITOKOTO Flash"
        self.dimensioni_titolo = 0.8
        self.panning_titolo = 200
        self.altezza_banda_titolo = (self.dimensioni_titolo*1000)+self.panning_titolo*2
        self.numero_foglio = 1
        self.stampa_titolo()

    def scrivi(self, testo):
       x = random.randrange(self.altezza_banda_titolo, self.p.margins.soft.right)
       y = random.randrange(self.p.margins.soft.top)
       dx = 0
       linee = []
       for linea in textwrap.wrap(testo,self.n_caratteri, replace_whitespace=False):
           linea = self.rimpiazza_accenti(linea)
           linea = linea.encode('latin1','replace')
           s = shapes.label(linea, self.dimensioni_carattere, self.altezza_carattere)
           transforms.rotate(s, pi/2)
           transforms.offset(s, (x+self.interlinea*dx,y))
           dx += 1
           linee.append(s)
       blocco = shapes.group(linee)
       tr_x = blocco.top_right.x
       #tr_y = blocco.top_right.y
       tr_y = y+self.w_colonna
       m_right = self.p.margins.soft.right
       m_top = self.p.margins.soft.top
       #print (m_right, m_top)
       if (tr_y > m_top):
           off = m_top-tr_y
           transforms.offset(blocco,(0,off))
       if (tr_x > m_right):
           off = m_right-tr_x
           transforms.offset(blocco,(off-120,0)) 
       self.p.write(blocco)
    
    '''
    def scrivi_linea(self, linea, x, y):
       s = shapes.label(linea.encode('latin1','replace'), 0.1, 0.2)
       transforms.rotate(s, pi/2)
       transforms.offset(s, (100*x+100,y))
       self.p.write(s)
    '''

    def rimpiazza_accenti(self, s):
        c = [(u'\xe0',"a'"),(u'\xe8',"e'"),(u'\xe9',"e'"),(u'\xec',"i'"),(u'\xf2',"o'"),(u'\xf9',"u'")]
        for i in c:
            s = s.replace(i[0],i[1])
        return s


    def mostra_foglio(self):
        io.view(self.p)

    def stampa_titolo(self):
        s = shapes.label(self.titolo + " | " + time.strftime("%d/%m/%Y") + " | " + "#" + str(self.numero_foglio), self.dimensioni_titolo, self.dimensioni_titolo*2)
        transforms.rotate(s, pi/2)
        transforms.offset(s, ((self.dimensioni_titolo*1000)+self.panning_titolo,self.panning_titolo*2))
        self.p.write(s)
        s = shapes.line((self.altezza_banda_titolo,100),(self.altezza_banda_titolo,self.p.margins.soft.top-100))
        self.p.write(s)
