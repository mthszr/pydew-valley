import pygame
from settings import *
from pytmx.util_pygame import load_pygame

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = position)
        self.z = LAYERS['soil']

class SoilLayer:
    def __init__(self, all_sprites):

        # Sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # Soil import
        self.soil_surface = pygame.image.load('./graphics/soil/o.png')

        self.create_soil_grid()
        self.create_hit_rect()

    def create_soil_grid(self):
        ground = pygame.image.load('./graphics/world/ground.png')
        h_tiles = ground.get_width() // TILE_SIZE
        v_tiles = ground.get_height() // TILE_SIZE

        self.grid = [[[] for _ in range(h_tiles)] for _ in range(v_tiles)]
        for x, y, _ in load_pygame('./data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')
    
    def create_hit_rect(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    SoilTile(
                        position = (index_col * TILE_SIZE, index_row * TILE_SIZE), 
                        surface = self.soil_surface, 
                        groups = [self.all_sprites, self.soil_sprites])