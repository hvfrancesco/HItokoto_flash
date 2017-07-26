from chiplotle import *
from chiplotle.tools.plottertools import instantiate_virtual_plotter
import ttfquery
from ttfquery import describe
from ttfquery import glyph
from flask import flash


class plotter_virtuale():
    def __init__(self):
        self.p = instantiate_virtual_plotter(type="HP7550A")
        self.p.margins.hard.draw_outline()

    def scrivi_linea(self, linea, y):
       flash(linea)
       s = shapes.label(linea.encode('latin1','replace'), 0.1, 0.2)
       transforms.offset(s, (100,100*y))
       self.p.write(s)


    def mostra_foglio(self):
        io.view(self.p)