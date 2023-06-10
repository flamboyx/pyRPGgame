import pygame
from settings import *
from entity import Entity
from support import import_folder
from particles import reflect_images

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.update_on = False

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-16, -24)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = enemy_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        self.attack_cooldown = monster_info['attack_cooldown']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300


    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': [], 'hit': []}
        main_path = f'images/enemies/{name}/'

        for animation in self.animations.keys():
            full_path = main_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_player_distance_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        return(distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            if 'left' in self.status:
                self.status = 'idle_left'
            else:
                self.status = 'idle'

        if distance <= max(WIDTH, HEIGHT):
            self.update_on = True
        else:
            self.update_on = False

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            if self.direction[0] < 0:
                self.status = 'attack_left'
                self.damage_player(self.damage, self.attack_type + '_left')
            else:
                self.damage_player(self.damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
            if self.direction[0] < 0:
                self.status = 'move_left'
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        if 'left' in self.status:
            animation = reflect_images(self.animations[self.status[0:-5]], 1, 0)
        else:
            animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            left = True
            if self.direction[0] < 0:
                left = False
            self.kill()
            if left:
                self.trigger_death_particles(self.rect.center, self.monster_name + '_left')
            else:
                self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
            if self.direction[0] < 0:
                self.status = 'hit'
            else:
                self.status = 'hit_left'


    def update(self):
        if self.update_on:
            self.hit_reaction()
            self.move(self.speed)
            self.animate()
            self.cooldowns()
            self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
