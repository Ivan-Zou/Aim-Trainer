import pygame
import math

class Target:
    PRIMARY_COLOR = "red"
    SECONDARY_COLOR = "white"

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def clicked(self, x, y):
        # checks if (x, y) is within the area of the target
        area = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return area <= self.size
    
    def draw(self, window):
        # draws the target onto the screen
        pygame.draw.circle(window, self.PRIMARY_COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(window, self.SECONDARY_COLOR, (self.x, self.y), self.size * 0.667)
        pygame.draw.circle(window, self.PRIMARY_COLOR, (self.x, self.y), self.size * 0.334)

    