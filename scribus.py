#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

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



def main(argv):
    """This is a documentation string. Write a description of what your code
    does here. You should generally put documentation strings ("docstrings")
    on all your Python functions."""
    url = "http://localhost:5000/api/storia"
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
    titolo_h = 10

    testo_x = 14
    testo_y = 62
    testo_w = 120
    testo_h = 134

    i=0

    for o in oggetti:
        scribus.newPage(-1)
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
        textbox = scribus.createText(testo_x, testo_y, testo_w, testo_h)
        scribus.insertText(o['body'],0,textbox)
        scribus.setTextColor('Black',textbox)
        scribus.setTextAlignment(scribus.ALIGN_BLOCK, textbox)
        scribus.setFont('Apple Garamond Regular', textbox)
        scribus.setFontSize(11, textbox)
        scribus.setLineSpacing(14, textbox)
        
        i += 1
        scribus.progressSet(i)

    scribus.progressReset()
    scribus.setUnit(userdim)
    scribus.docChanged(True)
    scribus.statusMessage("fatto")
    scribus.setRedraw(True)

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