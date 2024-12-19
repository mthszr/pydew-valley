import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite): 
    def __init__(self, position, group):  
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle' 
        self.frame_index = 0

        # Create the player
        self.image = self.animations[self.status][self.frame_index]
        self.rectangle = self.image.get_rect(center = position) # Set the player's position
        self.z = LAYERS['main']
        
        # Movement variables
        self.direction = pygame.math.Vector2() # The direction the player is moving
        self.position = pygame.math.Vector2(self.rectangle.center) # The player's position
        self.speed = 200

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

    def use_tool(self):
        pass
    
    def use_seed(self):
        pass
    
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

        if not self.timers['tool use'].active: # If the player is not using a tool
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

    # Move the player
    def move(self, dt):

        if self.direction.magnitude() > 0: # If the player is moving
            self.direction = self.direction.normalize() # Normalize the direction vector

        # Horizontal movement
        self.position.x += self.direction.x * self.speed * dt
        self.rectangle.centerx = self.position.x

        # Vertical movement
        self.position.y += self.direction.y * self.speed * dt
        self.rectangle.centery = self.position.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)

