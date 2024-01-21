import time

import pygame
from entity import Entity
from settings import *
from support import import_folder


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):

        # general setup
        super().__init__(groups)
        self.image = pygame.image.load('images/characters/main_character/down_idle/down_idle_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-8, -24)
        self.sprite_type = 'player'

        # graphics
        self.import_player_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # movement
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites

        # attacking
        self.attacking = False
        self.attack_cooldown = 200
        self.attack_time = 0
        self.can_attack = True

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 400

        # abilities
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health': 200, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6, 'recovery': 3}
        self.max_stats = {'health': 500, 'energy': 360, 'attack': 50, 'magic': 20, 'speed': 10, 'recovery': 9}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 150, 'magic': 150, 'speed': 200, 'recovery': 200}
        self.exp = 200
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 300

    def import_player_assets(self):
        character_path = 'images/characters/main_character/'
        self.animations = {'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_walk': [], 'down_walk': [], 'left_walk': [], 'right_walk': [],
                           'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right_walk'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left_walk'
            else:
                self.direction.x = 0

            if keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down_walk'
            elif keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up_walk'
            else:
                self.direction.y = 0

            if keys[pygame.K_SPACE] and not self.attacking and self.can_attack:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.can_attack = False

            if keys[pygame.K_e] and not self.attacking and self.can_attack:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']

                self.create_magic(style, strength, cost)
                self.can_attack = False

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_TAB] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status.replace('_walk', '_idle')

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0

            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                elif 'walk' in self.status:
                    self.status = self.status.replace('_walk', '_attack')
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '_idle')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.destroy_attack()
                self.attacking = False
        elif not keys[pygame.K_SPACE] and not keys[pygame.K_e]:
            self.can_attack = True

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']

        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']

        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
