import pygame
import random
import numpy as np


dirRange = [0, 360]
unitColour = [
    "#A411DA",  # pink
	"#377E65",  # green
	"#42AAFF",
    "#FF0000"
]

class unit:
    def __init__(self, unitID, width, height):
        self.unitID = unitID
        self.width = width
        self.height = height
        self.direction = random.uniform(
            np.radians(dirRange[0]),
            np.radians(dirRange[1])
        )
        self.position = np.array([random.uniform(0, width), random.uniform(0, height)])
        self.vel = np.array([np.cos(self.direction), np.sin(self.direction)])

        self.accel = np.array([0,0])
        self.accel_to_cohere = np.array([0, 0])
        self.accel_to_separate = np.array([0, 0])
        self.accel_to_align = np.array([0, 0])

        self.poly = np.array([(20, 0), (0, -5), (0, 5)])
        self.typeID = self.unitID%3
        self.colour = unitColour[self.typeID]

    def move(self):

        self.position += self.vel

        if self.position[0] > self.width or self.position[0] < 0:
            self.position[0] = np.abs(self.position - self.width)
        if self.position[1] > self.height or self.position[1] < 0:
            self.position[1] = np.abs(self.position - self.height)

    def display(self, screen):

        rotMatrix = np.array([[np.cos(self.direction), - np.sin(self.direction)], [np.sin(self.direction), np.cos(self.direction)]])
        
        rotPoly = np.dot(self.poly, rotMatrix.T) + self.position

        pygame.draw.polygon(screen, self.colour, rotPoly, 0)