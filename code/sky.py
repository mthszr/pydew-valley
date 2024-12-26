import pygame
from settings import *
from support import import_folder
from sprites import Generic
from random import randint, choice

class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)

    def display(self, dt):
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= 2 * dt

        self.full_surface.fill(self.start_color)
        self.display_surface.blit(self.full_surface, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)

class Drop(Generic):
    def __init__(self, surface, position, moving, groups, z):
        
        # General setup
        super().__init__(position, surface, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # Movement
        self.moving = moving
        if self.moving:
            self.position = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        # Movement
        if self.moving:
            self.position += self.direction * self.speed * dt
            self.rect.topleft = (round(self.position.x), round(self.position.y))

        # Timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('./graphics/rain/drops/')
        self.rain_floor = import_folder('./graphics/rain/floor/')
        self.floor_w, self.floor_h = pygame.image.load('./graphics/world/ground.png').get_size()

    def create_floor(self):
        Drop(
            surface = choice(self.rain_floor), 
            position = (randint(0, self.floor_w), randint(0, self.floor_h)), 
            moving = False, 
            groups = self.all_sprites, 
            z = LAYERS['rain floor'])

    def create_drops(self):
        Drop(
            surface = choice(self.rain_drops), 
            position = (randint(0, self.floor_w), randint(0, self.floor_h)), 
            moving = True, 
            groups = self.all_sprites, 
            z = LAYERS['rain drops'])

    def update(self):
        self.create_floor()
        self.create_drops()