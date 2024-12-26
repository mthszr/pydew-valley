import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite): 
    def __init__(self, position, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop):  
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle' 
        self.frame_index = 0

        # Create the player
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = position) 
        self.z = LAYERS['main']
        
        # Movement variables
        self.direction = pygame.math.Vector2() # The direction the player is moving
        self.position = pygame.math.Vector2(self.rect.center) # The player's position
        self.speed = 200

        # Collision 
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate((-126, -70))

        # Timer
        self.timers = {
            'tool use': Timer(350,self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350,self.use_seed),
            'seed switch': Timer(200)
        }     
        
        # Tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # Seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # Inventory
        self.item_inventory = {
            'wood':   0,
            'apple':  0,
            'corn':   0,
            'tomato': 0
        }
        self.seed_inventory = {
            'corn': 5,
            'tomato': 5
        }
        self.money = 200

        # Interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop

        # Sounds
        self.watering = pygame.mixer.Sound('./audio/water.mp3')
        self.watering.set_volume(0.2)

    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_position)

        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_position):
                    tree.damage()

        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_position)
            self.watering.play()

    def get_target_position(self):
        self.target_position = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]
    
    def use_seed(self):
        if self.seed_inventory[self.selected_seed] > 0:
            self.soil_layer.plant_seed(self.target_position, self.selected_seed)
            self.seed_inventory[self.selected_seed] -= 1
    
    def import_assets(self):
        # Import the player's animations
        self.animations = { 'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': [] }
        
        for animation in self.animations.keys():
            full_path = './graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt # Increase the frame index 
        if self.frame_index >= len(self.animations[self.status]): # If the frame index is greater than the length of the animation
            self.frame_index = 0 # Reset the frame index

        self.image = self.animations[self.status][int(self.frame_index)] # Set the image to the current frame
    
    # Get the input from the player
    def input(self): 
        keys = pygame.key.get_pressed() # Get the keys that are pressed

        if not self.timers['tool use'].active and not self.sleep: # If the player is not using a tool
            # Change the player's direction
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0 # If no keys are pressed, set the y direction to 0
            

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0 # If no keys are pressed, set the x direction to 0

            # Tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2() # Set the direction to 0
                self.frame_index = 0 # Guarantee the animation starts from the beginning

            # Change the selected tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                self.selected_tool = self.tools[self.tool_index % len(self.tools)]

            # Seed use
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2() # Set the direction to 0
                self.frame_index = 0 # Guarantee the animation starts from the beginning

            # Change the selected seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                self.selected_seed = self.seeds[self.seed_index % len(self.seeds)]

            if keys[pygame.K_RETURN]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Trader':
                        self.toggle_shop()
                    else:
                        self.status = 'left_idle'
                        self.sleep = True

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
    
    def get_status(self):
            # Idle animation
            if self.direction.magnitude() == 0:
                self.status = self.status.split('_')[0] + '_idle'

            # Tool animations
            if self.timers['tool use'].active:
                self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: # Moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: # Moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.position.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0: # Moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: # Moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.position.y = self.hitbox.centery

    # Move the player
    def move(self, dt):

        if self.direction.magnitude() > 0: # If the player is moving
            self.direction = self.direction.normalize() # Normalize the direction vector

        # Horizontal movement
        self.position.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # Vertical movement
        self.position.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')
        
    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_position()

        self.move(dt)
        self.animate(dt)

