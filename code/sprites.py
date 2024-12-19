import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rectangle = self.image.get_rect(topleft = position)
        self.z = z

