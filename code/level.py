import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import *

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame('./data/map.tmx')

        # House import
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surface in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surface in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites)

        # Fence import
        for x, y, surface in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surface, [self.all_sprites, self.collision_sprites])

        # Water import
        water_frames = import_folder('./graphics/water')
        for x, y, surface in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # Tree import
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], obj.name)
  
        # Wildflowers import
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])
    
        # Collision tiles
        for x, y, surface in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)
        
        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    position = (obj.x, obj.y), 
                    group = self.all_sprites, 
                    collision_sprites = self.collision_sprites,
                    tree_sprites = self.tree_sprites)
        Generic(
            position = (0,0),
            surface = pygame.image.load('./graphics/world/ground.png').convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS['ground'])

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
    def custom_draw(self, player):
        self.offset.x = player.rectangle.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rectangle.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rectangle.centery):
                if sprite.z == layer:
                    offset_rectangle = sprite.rectangle.copy()
                    offset_rectangle.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rectangle)

                    if sprite == player:
                        pygame.draw.rect(self.display_surface, 'red', offset_rectangle, 5)
                        hitbox_rectangle = player.hitbox.copy()
                        hitbox_rectangle.center = offset_rectangle.center
                        pygame.draw.rect(self.display_surface, 'green', hitbox_rectangle, 5)
                        target_position  = offset_rectangle.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                        pygame.draw.circle(self.display_surface, 'blue', target_position, 5)
