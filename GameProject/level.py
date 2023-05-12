import random

import pygame.math
from settings import *
from tile import Tile
from player import Player


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = DepthCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        rows = HEIGHT * 4 // 64 + 1
        cols = WIDTH * 4 // 64 + 1

        placeplayer = True

        for i in range(rows):
            j = 0
            while j < cols:
                col = random.randint(0, 1)
                x = j * TILESIZE
                y = i * TILESIZE
                if col == 1:
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 0 and placeplayer:
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                    placeplayer = False
                j += random.randint(1, 5)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class DepthCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)