'''
laser.py class.
'''
import pygame
import os
from functions.utils import collide  # Import from utils

# Load images
RED_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_yellow.png"))

# ... (other images)

class Laser:
    '''
    This class is used to define the characteristics of laserbeams shot by the player and enemies. 
    '''
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)
