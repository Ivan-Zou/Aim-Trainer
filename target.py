import pygame
import math

class Target:
    PRIMARY_COLOR = "red"
    SECONDARY_COLOR = "white"

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def hit(self, x, y):
            area = math.sqrt((x - self.x)**2 + (y - self.y)**2)
            return area <= self.size
    
    def draw(self, window):
        pygame.draw.circle(window, self.PRIMARY_COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(window, self.SECONDARY_COLOR, (self.x, self.y), self.size * 0.667)
        pygame.draw.circle(window, self.PRIMARY_COLOR, (self.x, self.y), self.size * 0.334)

    