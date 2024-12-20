import pygame
from settings import *
from random import randint, choice
from timer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rectangle = self.image.get_rect(topleft = position)
        self.z = z
        self.hitbox = self.rectangle.copy().inflate(-self.rectangle.width * 0.2, -self.rectangle.height * 0.75)

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
        self.hitbox = self.rectangle.copy().inflate(-20, -self.rectangle.height * 0.9)

class Tree(Generic):
    def __init__(self, position, surface, groups, name):
        super().__init__(position, surface, groups)

        # Tree atrributes
        self.health = 5
        self.alive = True
        stump_path = f'./graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surface = pygame.image.load(stump_path).convert_alpha()
        self.invvul_timer = Timer(200)

        # Apples
        self.apple_surface = pygame.image.load('./graphics/fruit/apple.png')
        self.apple_position = APPLE_POSITION[name]
        self.apple_sprites = pygame.sprite.Group()
        self.creat_fruits()

    def damage(self):
        
        # Damage the tree
        self.health -= 1
        
        # Remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            random_apple.kill()

    def creat_fruits(self):
        for position in self.apple_position:
            if randint(0, 10) < 2:
                x = position[0] + self.rectangle.left
                y = position[1] + self.rectangle.top
                Generic(
                    position = (x, y), 
                    surface = self.apple_surface, 
                    groups = [self.apple_sprites, self.groups()[0]],
                    z = LAYERS['fruit'])