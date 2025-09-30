import pygame
import pygame_widgets
import random
import numpy as np
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from unit import unit

def initialise(width, height):

  pygame.init()

  screen = pygame.display.set_mode((width, height))
  pygame.display.set_caption('Boids Demo')

  
  
  return width, height, screen

def genUnits(unitNum, unitList, width, height):

  for i in range(unitNum):
    unitList.append(unit(i, width, height))


  return unit

def distVectors(vectors):
  vectorNum = len(vectors)
  distList = [[0] * vectorNum for _ in range(vectorNum)]
  for i in range(vectorNum):
    distList[i][i] = (0,i)
    for j in range(vectorNum):
      if i < j:
        distance = np.linalg.norm(np.subtract(vectors[i], vectors[j]))
        distList[i][j] = (distance, j)
        distList[j][i] = (distance, i)

  return distList



def main():

  (width, height) = (400, 300)
  background_colour = (10,15,60)
  unitNum = 100
  unitList = []
  distList = []
  #seperation Power and Radius
  sepPow = 0.1
  sepRad = 25
  cohPow = .1
  cohRad = 200
  aliPow = .1
  aliRad = 100
  sliderHeight = 30
  sliderOffset = 25


  initParams = initialise(width, height)
  screen = initParams[2]

  #sepPowSlider = Slider(screen, sliderOffset, height - (sliderOffset*2 + sliderHeight), width-(sliderOffset*2), sliderHeight, max=10, min=0, step=0.1, handleRadius=5)
  #sepPowSliderTex = TextBox(screen, sliderOffset, height - (sliderOffset*2 + sliderHeight)*2, width-(sliderOffset*2), sliderHeight, fontSize=30)
  #sepPowSliderTex.disable()

  clock = pygame.time.Clock()
  genUnits(unitNum, unitList, width, height)


  while True:

    screen.fill(background_colour)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    

    #sepPowSliderTex.setText(sepPowSlider.getValue())


    distList = distVectors([unit.position for unit in unitList])

    for unit in unitList:
      unit.cohere(unitList, distList, cohPow, cohRad)
      unit.avoid(unitList, distList, sepPow, sepRad)
      unit.align(unitList, distList, aliPow, aliRad)
      unit.move()


    for unit in unitList:
      unit.display(screen)
    pygame_widgets.update(event)
    pygame.display.flip()
    clock.tick(60)



main()