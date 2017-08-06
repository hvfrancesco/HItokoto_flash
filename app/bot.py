import threading
import time
import pygame
from pygame.locals import *
import os
from .plot import plotter

class Scribus(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True  # OK for main to exit even if instance is still running
        self.paused = True  # start out paused
        self.state = threading.Condition()

    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified
            # do stuff, qui inserire gestione coda e plotter
            time.sleep(.1)
            # prova a produrre un pdf fresco ogni volta che si aggiunge una storia
            try:
                os.system('scribus-trunk -g -ns -py scribus.py  --  libro_a5.sla')
            except  OSError as e:
                if e.errno == os.errno.ENOENT:
                    pass
            self.pause()
            
    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait


class Worker(threading.Thread):
    def __init__(self,q):
        self.auto_pdf = True
        self.q = q
        self.p = plotter()
        threading.Thread.__init__(self)
        self.messaggio = "Premi un tasto per mettere il plotter in pausa e farlo ripartire\n"
        self.messaggio += "Premi 'q' per uscire\n"
        self.messaggio += "premi 'p' per visualizzare il plotter virtuale\n"
        self.messaggio += "premi 's' per stampare il titolo su un nuovo foglio"
        self.daemon = True  # OK for main to exit even if instance is still running
        self.paused = True  # start out paused
        self.state = threading.Condition()
        # da aggiungere: istanziare e far partire l'oggetto plot
        self.scribus = Scribus()
        self.scribus.start() # parte in pausa

    def run(self):
        self.resume() # unpause self
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified
            # do stuff, qui inserire gestione coda e plotter
            time.sleep(.1)
            if not self.q.empty():
                # prova a produrre un pdf fresco ogni volta che si aggiunge una storia
                #try:
                #    os.system('scribus-trunk -g -ns -py scribus.py  --  libro_a5.sla')
                #except  OSError as e:
                #    if e.errno == os.errno.ENOENT:
                #        pass
                if self.auto_pdf:
                    self.scribus.resume() # se auto_pdf impostato, produce nuovo libro pdf ad ogni nuova storia
                storia = self.q.get()
                self.p.scrivi(storia[1])
                self.messaggio = "storia ricevuta da: "+storia[0]+'\n'+storia[1] # messaggio da mostrare nella finestra controllo


    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting
            print "attivo"

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait
            print "in pausa"


class Controller(threading.Thread):
    def __init__(self, worker):
        self.worker = worker
        threading.Thread.__init__(self)
        self.daemon = True  # OK for main to exit even if instance is still running
        self.paused = True  # start out paused
        self.state = threading.Condition()
        self.img_on = pygame.image.load('hito_on.png')
        self.img_off = pygame.image.load('hito_off.png')
        self.white = (255, 255, 255)
        pygame.init()
        pygame.font.init()
        self.guifont_name = 'static/fonts/Roboto-Light.ttf'
        self.guifont_url = os.path.join(os.path.dirname(__file__),self.guifont_name)
        self.guifont = pygame.font.Font(self.guifont_url,11)
        self.screen = pygame.display.set_mode((480, 600))
        self.screen.fill((self.white))
        self.screen.blit(self.img_on, (0,0))
        #self.pygame_text = self.guifont.render(self.worker.messaggio, True, (0, 0, 0))
        self.pygame_text = self.multiLineSurface(self.worker.messaggio, self.guifont, pygame.Rect(10,200,460,500), (0,0,0), (255,255,255))
        self.screen.blit(self.pygame_text,(10,220))
        pygame.display.set_caption('Hitokoto')
        pygame.mouse.set_visible(0)
        self.condition = True
        self.vai = True

    def run(self):
        self.resume() # unpause self
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified
            while self.vai:
                self.screen.fill((self.white))
                if self.condition:
                    self.img = self.img_on
                else:
                    self.img = self.img_off
                self.screen.blit(self.img,(0,0))
                #self.pygame_text = self.guifont.render(self.worker.messaggio, True, (0, 0, 0))
                self.pygame_text = self.multiLineSurface(self.worker.messaggio, self.guifont, pygame.Rect(10,200,460,500), (0,0,0), (255,255,255))
                self.screen.blit(self.pygame_text,(10,220))
                pygame.display.flip()
                time.sleep(.1)
                for event in pygame.event.get():
                    if (event.type == KEYDOWN):
                        if (event.key == pygame.K_q):
                            self.vai = False
                            os._exit(0)
                            break
                        elif (event.key == pygame.K_p):
                            self.mostra_foglio_virtuale()
                        elif (event.key == pygame.K_s):
                            self.stampa_titolo_tavola()
                        elif (event.key == pygame.K_b):
                            self.produci_pdf()
                        elif (event.key == pygame.K_a):
                            self.toggle_auto_pdf()
                        else:
                            time.sleep(0.1)
                            self.pausa()
    
    def mostra_foglio_virtuale(self):
        self.worker.p.mostra_foglio()
        self.worker.messaggio = "Mostro il foglio del plotter virtuale" 
    
    def stampa_titolo_tavola(self):
        self.worker.p.numero_foglio += 1 # stampa il titolo su un nuovo foglio
        self.worker.p.stampa_titolo() # con un numero progressivo
        self.worker.messaggio = "Ho stampato il titolo su un nuovo foglio"
    
    #def produci_pdf(self):
    #    try:
    #        os.system('scribus-trunk -g -ns -py scribus.py  --  libro_a5.sla')
    #    except  OSError as e:
    #        if e.errno == os.errno.ENOENT:
    #            pass
    
    def produci_pdf(self):
        self.worker.scribus.resume()


    def toggle_auto_pdf(self):
        self.worker.auto_pdf = not self.worker.auto_pdf
        if self.worker.auto_pdf:
            self.worker.messaggio = "auto PDF abilitato"
        else:
            self.worker.messaggio = "auto PDF disabilitato"
    
    
    def pausa(self):
        self.condition = not self.condition
        if self.condition:
            self.worker.resume()
        else:
            self.worker.pause()


    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait

    
    
    class TextRectException:
        def __init__(self, message=None):
            self.message = message

        def __str__(self):
            return self.message


    def multiLineSurface(self, string, font, rect, fontColour, BGColour, justification=0):
        """Returns a surface containing the passed text string, reformatted
        to fit within the given rect, word-wrapping as necessary. The text
        will be anti-aliased.

        Parameters
        ----------
        string - the text you wish to render. \n begins a new line.
        font - a Font object
        rect - a rect style giving the size of the surface requested.
        fontColour - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
        BGColour - a three-byte tuple of the rgb value of the surface.
        justification - 0 (default) left-justified
                    1 horizontally centered
                   2 right-justified

        Returns
        -------
        Success - a surface object with the text rendered onto it.
        Failure - raises a TextRectException if the text won't fit onto the surface.
        """

        finalLines = []
        requestedLines = string.splitlines()
        # Create a series of lines that will fit on the provided
        # rectangle.
        for requestedLine in requestedLines:
            if font.size(requestedLine)[0] > rect.width:
                words = requestedLine.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        raise self.TextRectException("The word " + word + " is too long to fit in the rect passed.")
                # Start a new line
                accumulatedLine = ""
                for word in words:
                    testLine = accumulatedLine + word + " "
                    # Build the line while the words fit.
                    if font.size(testLine)[0] < rect.width:
                        accumulatedLine = testLine
                    else:
                        finalLines.append(accumulatedLine)
                        accumulatedLine = word + " "
                finalLines.append(accumulatedLine)
            else:
                finalLines.append(requestedLine)

        # Let's try to write the text out on the surface.
        surface = pygame.Surface(rect.size)
        surface.fill(BGColour)
        accumulatedHeight = 0
        for line in finalLines:
            #if accumulatedHeight + font.size(line)[1] >= rect.height:
                #raise self.TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
            if line != "":
                tempSurface = font.render(line, 1, fontColour)
            if justification == 0:
                surface.blit(tempSurface, (0, accumulatedHeight))
            elif justification == 1:
                surface.blit(tempSurface, ((rect.width - tempSurface.get_width()) / 2, accumulatedHeight))
            elif justification == 2:
                surface.blit(tempSurface, (rect.width - tempSurface.get_width(), accumulatedHeight))
            else:
                raise self.TextRectException("Invalid justification argument: " + str(justification))
            accumulatedHeight += font.size(line)[1]
        return surface