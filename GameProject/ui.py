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

        # convert weapon dict
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.transform.scale_by(pygame.image.load(path).convert_alpha(), 2)
            self.weapon_graphics.append(weapon)

        # convert magic dict
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current_amount, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.x += 2
        current_rect.y += 2
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, 'black', bg_rect, 4)
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, current_rect, 2)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 10
        text_rect = text_surf.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(10, 0))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 0), 2)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 2)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 2)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(self.display_surface.get_size()[0] - 110, 10, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index].convert_alpha()
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(self.display_surface.get_size()[0] - 205, 15, has_switched)
        magic_surf = pygame.transform.scale_by(self.magic_graphics[magic_index].convert_alpha(), 2)
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar, ENERGY_COLOR)

        self.show_exp(player.exp)

        self.magic_overlay(player.magic_index, not player.can_switch_magic)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
