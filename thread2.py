#!/usr/bin/env python


import pygame
from pygame.locals import *

import threading
import time

img_on = pygame.image.load('hito_on.png')
img_off = pygame.image.load('hito_off.png')
white = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((480, 200))
screen.fill((white))
screen.blit(img_on,(0,0))
pygame.display.set_caption('Hitokoto')
pygame.mouse.set_visible(0)

class Concur(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.iterations = 0
        self.daemon = True  # OK for main to exit even if instance is still running
        self.paused = True  # start out paused
        self.state = threading.Condition()

    def run(self):
        self.resume() # unpause self
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified
            # do stuff
            time.sleep(.1)
            self.iterations += 1
            print self.iterations

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait


concur = Concur()
concur.start() # calls run() method

condition = True
vai = True

while vai:
  screen.fill((white))
  if condition:
      img = img_on
  else:
      img = img_off
  screen.blit(img,(0,0))
  pygame.display.flip()
  print "culo!"
  time.sleep(.1)
  for event in pygame.event.get():
      if (event.type == KEYDOWN):
		if (event.key == pygame.K_q):
			vai = False
			break
		print "key pressed"
		time.sleep(0.1)
		condition = not condition
		print condition
		if condition:
			 concur.resume()
		else:
			 concur.pause()
			


print('concur.iterations == {}'.format(concur.iterations))  # show thread executed
