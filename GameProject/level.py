import pygame
import random
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        rows = HEIGHT // 64 + 1
        cols = WIDTH // 64 + 1

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
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()