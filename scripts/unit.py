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
        self.accel_to_avoid = np.array([0, 0])
        self.accel_to_align = np.array([0, 0])

        self.poly = np.array([(20, 0), (0, -5), (0, 5)])
        self.typeID = self.unitID%3
        self.colour = unitColour[self.typeID]

    def move(self):

        self.accel = self.accel_to_align + self.accel_to_cohere + self.accel_to_avoid

        vector = self.vel + self.accel
        self.vel = (vector) / np.linalg.norm(vector)
        self.direction = np.arctan2(self.vel[1], self.vel[0])
        self.position += self.vel

        if self.position[0] > self.width or self.position[0] < 0:
            self.position[0] = np.abs(self.position[0] - self.width)
        if self.position[1] > self.height or self.position[1] < 0:
            self.position[1] = np.abs(self.position[1] - self.height)

    def cohere(self, unitList, distance, power, radius):
        nearUnitsList = [
            d[1] for d in distance[self.unitID]
            if 0 < d[0] < radius and unitList[d[1]].colour == self.colour
            ]
        if len(nearUnitsList) > 0:
            nearUnit = [unitList[unitID] for unitID in nearUnitsList]
            centerOfNear = np.mean(np.array([unit.position for unit in nearUnit]))
            vector = np.subtract(centerOfNear, self.position)

            self.accel_to_cohere =  power * (vector / np.linalg.norm(vector))
        else:
            self.accel_to_cohere = np.array([0,0])

    def avoid(self, unitList, distance, power, radius):
        nearUnitsList = [
            d[1] for d in distance[self.unitID]
            if 0 < d[0] < radius
        ]
        if len(nearUnitsList) > 0:
            nearUnit = [unitList[unitID] for unitID in nearUnitsList]
            centerOfNear = np.mean(np.array([unit.position for unit in nearUnit]))
            vector = np.subtract(centerOfNear, self.position)

            self.accel_to_avoid = - power * (vector / np.linalg.norm(vector))
        else:
            self.accel_to_avoid = np.array([0,0])
                      
    def align(self, unitList, distance, power, radius):
        nearUnitsList = [
            d[1] for d in distance[self.unitID]
            if 0 < d[0] < radius and unitList[d[1]].colour == self.colour
            ]
        if len(nearUnitsList) > 0:
            nearUnit = [unitList[unitID] for unitID in nearUnitsList]
            vector = np.sum([unit.vel for unit in nearUnit], axis=0)

            self.accel_to_align =  power * (vector / np.linalg.norm(vector))
        else:
            self.accel_to_align = np.array([0,0])



    def display(self, screen):

        rotMatrix = np.array([[np.cos(self.direction), -np.sin(self.direction)],[np.sin(self.direction), np.cos(self.direction)]])
        
        rotPoly = np.dot(self.poly, rotMatrix.T) + self.position

        pygame.draw.polygon(screen, self.colour, rotPoly, 0)