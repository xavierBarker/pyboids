import pygame
import numpy as np

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