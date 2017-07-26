import threading
import time
import pygame
from pygame.locals import *


class Concur(threading.Thread):
    def __init__(self,q):
        self.q = q
        threading.Thread.__init__(self)
        self.iterations = 0
        self.daemon = True  # OK for main to exit even if instance is still running
        self.paused = True  # start out paused
        self.state = threading.Condition()
        # da aggiungere: istanziare e far partire l'oggetto plot

    def run(self):
        self.resume() # unpause self
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified
            # do stuff, qui inserire gestione coda e plotter
            time.sleep(.1)
            self.iterations += 1
            print self.iterations
            if not self.q.empty():
                print self.q.get()

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait


class Controller(threading.Thread):
    def __init__(self, concur):
        self.concur = concur
        threading.Thread.__init__(self)
        self.daemon = True  # OK for main to exit even if instance is still running
        self.paused = True  # start out paused
        self.state = threading.Condition()

        self.img_on = pygame.image.load('hito_on.png')
        self.img_off = pygame.image.load('hito_off.png')
        self.white = (255, 255, 255)
        pygame.init()
        self.screen = pygame.display.set_mode((480, 200))
        self.screen.fill((self.white))
        self.screen.blit(self.img_on, (0,0))
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
                pygame.display.flip()
                print "culo!"
                time.sleep(.1)
                for event in pygame.event.get():
                    if (event.type == KEYDOWN):
		                if (event.key == pygame.K_q):
			                self.vai = False
			                break
		                print "key pressed"
		                time.sleep(0.1)
		                self.condition = not self.condition
		                print self.condition
		                if self.condition:
			                self.concur.resume()
		                else:
			                self.concur.pause()
			
            print('concur.iterations == {}'.format(self.concur.iterations))  # show thread executed


    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait

