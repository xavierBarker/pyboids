import pygame
import random
import numpy as np

from unit import unit

def initialise():

    pygame.init()

    background_colour = (10,15,60)
    (width, height) = (600, 400)


    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Boids Demo')
    screen.fill(background_colour)

    pygame.display.flip()


    running = True

    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False

def main():

    unitNum = 100

    initialise()

    


main()