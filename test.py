#!/usr/bin/env python

from chiplotle import *
from chiplotle.tools.plottertools import instantiate_virtual_plotter
import ttfquery
from ttfquery import describe
from ttfquery import glyph

p =  instantiate_virtual_plotter(type="HP7550A")


font_url = "./1CamBam_Stick_2.ttf"
f = describe.openFont(font_url)

caratteri = ("f", "a", "d", "e", " ", "A", ",", ";")
lettere = {}

for c in caratteri:
    g = glyph.Glyph(ttfquery.glyphquery.glyphName(f,c))
    contours = g.calculateContours(f)
    forme = []
    for contour in contours:
        line = ttfquery.glyph.decomposeOutline(contour)
        shape = shapes.path(line)
        forme.append(shape)
    gruppo = shapes.group(forme)
    lettere[c]=gruppo
    
    #test
    p.write(gruppo)

print lettere["A"].width

prova = lettere['f']
transforms.offset(prova,(1000,1000))

p.write(prova)

io.view(p)
