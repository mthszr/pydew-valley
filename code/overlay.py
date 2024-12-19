import pygame
from settings import *

class Overlay:
    def __init__(self,player):
        
        # General setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # Import the overlay assets
        overlay_path = './graphics/overlay/'
        self.tools_surface = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surface = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}
        
    def display(self):

        # Display the tools
        tool_surface = self.tools_surface[self.player.selected_tool]
        tool_rectangle = tool_surface.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surface, tool_rectangle)

        # Display the seeds
        seed_surface = self.seeds_surface[self.player.selected_seed]
        seed_rectangle = seed_surface.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surface, seed_rectangle)