import pygame
from settings import *
from random import randint, choice
from timer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = position)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Interaction(Generic):
    def __init__(self, position, size, groups, name):
        surface = pygame.Surface(size)
        super().__init__(position, surface, groups)
        self.name = name

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
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class Particle(Generic):
    def __init__(self, position, surface, groups, z, duration = 200):
        super().__init__(position, surface, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # White surface
        mask_surface = pygame.mask.from_surface(self.image)
        new_surface = mask_surface.to_surface()
        new_surface.set_colorkey((0, 0, 0))
        self.image = new_surface

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

class Tree(Generic):
    def __init__(self, position, surface, groups, name, player_add):
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
        self.create_fruits()

        self.player_add = player_add

    def damage(self):
        
        # Damage the tree
        self.health -= 1
        
        # Remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(
                position = random_apple.rect.topleft, 
                surface = random_apple.image, 
                groups = self.groups()[0], 
                z = LAYERS['fruit'])
            self.player_add('apple')
            random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            Particle(
                position = self.rect.topleft,
                surface = self.image,
                groups = self.groups()[0],
                z = LAYERS['fruit'],
                duration = 300
            )
            self.image = self.stump_surface
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add('wood')

    def update(self, dt):
        if self.alive:
            self.check_death()

    def create_fruits(self):
        for position in self.apple_position:
            if randint(0, 10) < 2:
                x = position[0] + self.rect.left
                y = position[1] + self.rect.top
                Generic(
                    position = (x, y), 
                    surface = self.apple_surface, 
                    groups = [self.apple_sprites, self.groups()[0]],
                    z = LAYERS['fruit'])