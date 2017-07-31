#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

try:
    # Please do not use 'from scribus import *' . If you must use a 'from import',
    # Do so _after_ the 'import scribus' and only import the names you need, such
    # as commonly used constants.
    import scribus
except ImportError,err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)

import requests
import json
from datetime import datetime


def main(argv):
    """This is a documentation string. Write a description of what your code
    does here. You should generally put documentation strings ("docstrings")
    on all your Python functions."""
    t_format = "%Y-%m-%dT%H:%M:%S.%f"
    local_format = "%d-%m-%Y %H:%M:%S"
    url = "http://localhost:5000/api/storia"
    url_autore = "http://localhost:5000/api/autore"
    headers = {'Accept': 'application/vnd.api+json'}
    post_headers = {'Accept': 'application/vnd.api+json', 'Content-Type': 'application/vnd.api+json'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    risposta = response.json()
    oggetti = risposta['objects']

    userdim = scribus.getUnit()
    scribus.setUnit(scribus.UNIT_MM)
    scribus.progressTotal(len(oggetti))
    scribus.setRedraw(False)

    nome_x = 60
    nome_y = 39
    nome_w = 74
    nome_h = 6

    titolo_x = 60
    titolo_y = 46
    titolo_w = 74
    titolo_h = 6

    tz_x = 60
    tz_y = 52
    tz_w = 74
    tz_h = 6

    testo_x = 14
    testo_y = 62
    testo_w = 120
    testo_h = 134

    pag_x = 14
    pag_y = 14
    pag_w = 120
    pag_h = 182

    i=0

    for o in oggetti:
        scribus.newPage(-1)
        textbox = scribus.createText(nome_x, nome_y, nome_w, nome_h)
        scribus.insertText(o['autore']['nome'],0,textbox)
        scribus.setTextColor('Black',textbox)
        scribus.setTextAlignment(scribus.ALIGN_RIGHT, textbox)
        scribus.setFont('Myriad Pro Bold', textbox)
        scribus.setFontSize(14, textbox)
        scribus.setLineSpacing(16, textbox)

        if o['titolo'] != "":
            textbox = scribus.createText(titolo_x, titolo_y, titolo_w, titolo_h)
            scribus.insertText(o['titolo'],0,textbox)
            scribus.setTextColor('Black',textbox)
            scribus.setTextAlignment(scribus.ALIGN_RIGHT, textbox)
            scribus.setFont('Myriad Pro Italic', textbox)
            scribus.setFontSize(14, textbox)
            scribus.setLineSpacing(16, textbox)
        
        if o['timestamp']:
            tempo = o['timestamp'][:-7]
            data = tempo.split("T")[0]
            tempo = tempo.split("T")[1]
            data = data.split("-")
            data = data[2]+"-"+data[1]+"-"+data[0]
            tempo = data + " alle ore " + tempo
            textbox = scribus.createText(tz_x, tz_y, tz_w, tz_h)
            scribus.insertText(tempo,0,textbox)
            scribus.setTextColor('Black',textbox)
            scribus.setTextAlignment(scribus.ALIGN_RIGHT, textbox)
            scribus.setFont('Myriad Pro Italic', textbox)
            scribus.setFontSize(11, textbox)
            scribus.setLineSpacing(14, textbox)

        corpo_testo = scribus.createText(testo_x, testo_y, testo_w, testo_h)
        scribus.insertText(o['body'],0,corpo_testo)
        scribus.setTextColor('Black',corpo_testo)
        scribus.setTextAlignment(scribus.ALIGN_BLOCK, corpo_testo)
        scribus.setFont('Apple Garamond Regular', corpo_testo)
        scribus.setFontSize(11, corpo_testo)
        scribus.setLineSpacing(14, corpo_testo)

        scribus.newPage(-1)
        if scribus.textOverflows(corpo_testo, 1):
            overflow_testo = scribus.createText(pag_x, pag_y, pag_w, pag_h)
            scribus.setTextColor('Black',overflow_testo)
            scribus.setTextAlignment(scribus.ALIGN_BLOCK, overflow_testo)
            scribus.setFont('Apple Garamond Regular', overflow_testo)
            scribus.setFontSize(11, overflow_testo)
            scribus.setLineSpacing(14, overflow_testo)
            scribus.linkTextFrames(corpo_testo, overflow_testo)
            if scribus.textOverflows(overflow_testo, 1):
                scribus.newPage(-1)
                overflow_testo_2 = scribus.createText(pag_x, pag_y, pag_w, pag_h)
                scribus.setTextColor('Black',overflow_testo_2)
                scribus.setTextAlignment(scribus.ALIGN_BLOCK, overflow_testo_2)
                scribus.setFont('Apple Garamond Regular', overflow_testo_2)
                scribus.setFontSize(11, overflow_testo_2)
                scribus.setLineSpacing(14, overflow_testo_2)
                scribus.linkTextFrames(overflow_testo, overflow_testo_2)
                scribus.newPage(-1)
                if scribus.textOverflows(overflow_testo_2, 1):
                    overflow_testo_3 = scribus.createText(pag_x, pag_y, pag_w, pag_h)
                    scribus.setTextColor('Black',overflow_testo_3)
                    scribus.setTextAlignment(scribus.ALIGN_BLOCK, overflow_testo_3)
                    scribus.setFont('Apple Garamond Regular', overflow_testo_3)
                    scribus.setFontSize(11, overflow_testo_3)
                    scribus.setLineSpacing(14, overflow_testo_3)
                    scribus.linkTextFrames(overflow_testo_2, overflow_testo_3)
                    
        
        i += 1
        scribus.progressSet(i)


    for p in range(4-(scribus.pageCount()%4)):
        scribus.newPage(-1)
    
    # prima pagina
    response = requests.get(url_autore, headers=headers)
    assert response.status_code == 200
    risposta = response.json()
    oggetti = risposta['objects']
    scribus.gotoPage(1)
    textbox = scribus.createText(60, 85, 74, 12)
    scribus.insertText("HITOKOTO Flash",0,textbox)
    scribus.setTextColor('Black',textbox)
    scribus.setTextAlignment(scribus.ALIGN_RIGHT, textbox)
    scribus.setFont('Myriad Pro Bold', textbox)
    scribus.setFontSize(14, textbox)
    scribus.setLineSpacing(16, textbox)
    box_autori = scribus.createText(60, 102, 74, 94)
    box_autori_testo = "con scritti di:\n"
    for o in oggetti:
        box_autori_testo += "- "
        box_autori_testo += o['nome']
        box_autori_testo += "\n"
    scribus.insertText(box_autori_testo,0,box_autori)
    scribus.setTextColor('Black',box_autori)
    scribus.setTextAlignment(scribus.ALIGN_RIGHT, box_autori)
    scribus.setFont('Myriad Pro Italic', box_autori)
    scribus.setFontSize(11, box_autori)
    scribus.setLineSpacing(14, box_autori)

    # ultima pagina
    scribus.gotoPage(scribus.pageCount())
    textbox = scribus.createText(14, 180, 120, 14)
    scribus.insertText("HITOKOTO Flash",0,textbox)
    scribus.setTextColor('Black',textbox)
    scribus.setTextAlignment(scribus.ALIGN_CENTERED, textbox)
    scribus.setFont('Myriad Pro Bold', textbox)
    scribus.setFontSize(11, textbox)
    scribus.setLineSpacing(14, textbox)

    scribus.progressReset()
    scribus.setUnit(userdim)
    scribus.docChanged(True)
    scribus.statusMessage("fatto")
    scribus.setRedraw(True)

    nome_pdf = "libro_a5.pdf"
    pdf = scribus.PDFfile(outdst=1,version=15, file = nome_pdf, fonts=('Myriad Pro Italic','Apple Garamond Regular', 'Myriad Pro Bold', 'Myriad Pro Italic'))
    pdf.save()

    os.system("./prepara_pdf.sh " + nome_pdf)

def main_wrapper(argv):
    """The main_wrapper() function disables redrawing, sets a sensible generic
    status bar message, and optionally sets up the progress bar. It then runs
    the main() function. Once everything finishes it cleans up after the main()
    function, making sure everything is sane before the script terminates."""
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        # Exit neatly even if the script terminated with an exception,
        # so we leave the progress bar and status bar blank and make sure
        # drawing is enabled.
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()

# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
    main_wrapper(sys.argv)