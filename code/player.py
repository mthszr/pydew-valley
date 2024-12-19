import pygame
from settings import *

class Player(pygame.sprite.Sprite): 
    def __init__(self, position, group):  
        super().__init__(group)

        # Create the player
        self.image = pygame.Surface((32, 64)) # Create a surface for the player
        self.image.fill('green') # Fill the player with green color
        self.rect = self.image.get_rect(center = position) # Set the player's position

        # Movement variables
        self.direction = pygame.math.Vector2() # The direction the player is moving
        self.position = pygame.math.Vector2(self.rect.center) # The player's position
        self.speed = 200

    def import_assets(self):
        self.animations = { 
        
        }
    
    # Get the input from the player
    def input(self): 
        keys = pygame.key.get_pressed() # Get the keys that are pressed

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0 # If no keys are pressed, set the y direction to 0
        

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0 # If no keys are pressed, set the x direction to 0

    # Move the player
    def move(self, dt):

        if self.direction.magnitude() > 0: # If the player is moving
            self.direction = self.direction.normalize() # Normalize the direction vector

        # Horizontal movement
        self.position.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.position.x

        # Vertical movement
        self.position.y += self.direction.y * self.speed * dt
        self.rect.centery = self.position.y

    def update(self, dt):
        self.input()
        self.move(dt)

