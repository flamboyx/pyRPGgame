import random

import pygame.math
from enemy import Enemy
from player import Player
from tile import Tile
from weapon import Weapon
from ui import UI
from particles import AnimationPlayer
from settings import *
from support import *
from random import randint



class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = DepthCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('maps/map2/RPG_Forest_Boundary.csv'),
            'backflora': import_csv_layout('maps/map2/RPG_Forest_BackFlora.csv'),
            'frontflora': import_csv_layout('maps/map2/RPG_Forest_FrontFlora.csv'),
            'grass': import_csv_layout('maps/map2/RPG_Forest_Grass.csv'),
            'entities': import_csv_layout('maps/map2/RPG_Forest_Entities.csv')
        }

        graphics = {
            'flora': import_folder('images/graphics/flora')
        }

        obstacles = []

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
                            if int(col) in obstacles:
                                Tile((x, y),
                                     [self.visible_sprites, self.obstacle_sprites],
                                     'flora',
                                     surface)
                            else:
                                Tile((x, y),
                                     [self.visible_sprites],
                                     'flora',
                                     surface)
                        if style == 'flora':
                            surface = graphics['flora'][int(col)]
                            if int(col) in obstacles:
                                Tile((x, y),
                                     [self.visible_sprites, self.obstacle_sprites],
                                     'flora',
                                     surface)
                            else:
                                Tile((x, y),
                                     [self.visible_sprites],
                                     'flora',
                                     surface)
                        if style == 'frontflora':
                            surface = graphics['flora'][int(col)]
                            if int(col) in obstacles:
                                Tile((x, y),
                                     [self.visible_sprites, self.obstacle_sprites],
                                     'flora',
                                     surface)
                            else:
                                Tile((x, y),
                                     [self.visible_sprites],
                                     'flora',
                                     surface)
                        if style == 'grass':
                            surface = graphics['flora'][int(col)]
                            Tile((x, y),
                                 [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                 'grass',
                                 surface)
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
                                Enemy(monster_name,
                                      (x, y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player)
        self.player = Player((100, 100),
                             [self.visible_sprites],
                             self.obstacle_sprites,
                             self.create_attack,
                             self.destroy_attack,
                             self.create_magic)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        print(style)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            for grass in range(randint(2, 4)):
                                self.animation_player.create_grass_particles(pos, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)


class DepthCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load('images/tilemaps/ground_2.bmp').convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface,
                                                    (self.floor_surface.get_size()[0] * 2,
                                                     self.floor_surface.get_size()[1] * 2))
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
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type')
                         and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)
