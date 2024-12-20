import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rectangle = self.image.get_rect(topleft = position)
        self.z = z

class Water(Generic):
    def __init__(self, position, frames, groups):
        
        # Animation setup
        self.frames = frames
        self.frame_index = 0

        # Sprite setup
        super().__init__(
            position = position, 
            surface = self.frames[self.frame_index], 
            groups =  groups, 
            z = LAYERS['water'])
        
    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class WildFlower(Generic):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups)

class Tree(Generic):
    def __init__(self, position, surface, groups, name):
        super().__init__(position, surface, groups)