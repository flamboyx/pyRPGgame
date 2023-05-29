import pygame
from settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
        self.energy_bar = pygame.Rect(10, 35, ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT)

    def show_bar(self, current_amount, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.x += 2
        current_rect.y += 2
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 2)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar, ENERGY_COLOR)