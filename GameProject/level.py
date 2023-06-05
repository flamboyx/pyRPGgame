import random

import pygame.math
from enemy import Enemy
from player import Player
from tile import Tile
from weapon import Weapon
from ui import UI
from settings import *
from support import *



class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = DepthCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_village_Boundary.csv'),
            'backflora': import_csv_layout('map/map_village_BackFlora.csv'),
            'flora': import_csv_layout('map/map_village_Flora.csv'),
            'frontflora': import_csv_layout('map/map_village_FrontFlora.csv'),
            'backprops': import_csv_layout('map/map_village_BackProps.csv'),
            'props': import_csv_layout('map/map_village_Props.csv'),
            'houses': import_csv_layout('map/map_village_Houses.csv'),
            'entities': import_csv_layout('map/map_village_Entities.csv')
        }

        graphics = {
            'flora': import_folder('images/graphics/flora')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'backflora':
                            surface = graphics['flora'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'flora', surface)
                        if style == 'flora':
                            surface = graphics['flora'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'flora', surface)
                        if style == 'frontflora':
                            surface = graphics['flora'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'flora', surface)
                        if style == 'entities':
                            if col == '1':
                                self.player = Player((x, y),
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic)
                            else:
                                if col == '2': monster_name = 'bat'
                                elif col == '3': monster_name = 'jaws'
                                Enemy(monster_name, (x, y), [self.visible_sprites], self.obstacle_sprites)

    def create_attack(self):
        self.attack_time = pygame.time.get_ticks()
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def create_magic(self, style, strength, cost):
        print(style)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)


class DepthCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load('images/tilemaps/ground_1.png').convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface, (self.floor_surface.get_size()[0] * 2, self.floor_surface.get_size()[1] * 2))
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)
