import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *

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
        self.soil_surfaces = import_folder_dict('./graphics/soil/')

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

                    # Check for adjacent soil tiles
                    top = 'X' in self.grid[index_row - 1][index_col]
                    bottom = 'X' in self.grid[index_row + 1][index_col]
                    right = 'X' in row[index_col + 1]
                    left = 'X' in row[index_col - 1]

                    tile_type = 'o'

                    # All sides are soil
                    if all((top, bottom, right, left)): tile_type = 'x'

                    # Horizontal soil
                    if left and not any((top, right, bottom)): tile_type = 'r'
                    if right and not any((top, left, bottom)): tile_type = 'l'
                    if right and left and not any((top, bottom)): tile_type = 'lr'

                    # Vertical soil
                    if top and not any((left, right, bottom)): tile_type = 'b'
                    if bottom and not any((top, left, right)): tile_type = 't'
                    if top and bottom and not any((left, right)): tile_type = 'tb'

                    # Corners
                    if left and bottom and not any((top, right)): tile_type = 'tr'
                    if right and bottom and not any((top, left)): tile_type = 'tl'
                    if left and top and not any((right, bottom)): tile_type = 'br'
                    if right and top and not any((left, bottom)): tile_type = 'bl'

                    # T shaped
                    if all((top, bottom, right)) and not left: tile_type = 'tbr'
                    if all((top, bottom, left)) and not right: tile_type = 'tbl'
                    if all((left, right, top)) and not bottom: tile_type = 'lrb'
                    if all((left, right, bottom)) and not top: tile_type = 'lrt'

                    SoilTile(
                        position = (index_col * TILE_SIZE, index_row * TILE_SIZE), 
                        surface = self.soil_surfaces[tile_type], 
                        groups = [self.all_sprites, self.soil_sprites])