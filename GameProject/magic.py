import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):
        if player.health < player.stats['health']:
            if player.energy >= cost:
                player.health += strength
                player.energy -= cost
                if player.health >= player.stats['health']:
                    player.health = player.stats['health']
                if player.direction.x > 0:
                    self.animation_player.create_particles('heal_bubbles',
                                                           player.rect.center + pygame.math.Vector2(0,20), groups)
                    self.animation_player.create_particles('heal', player.rect.center, groups)
                else:
                    self.animation_player.create_particles('heal_bubbles_left',
                                                           player.rect.center + pygame.math.Vector2(0, 20), groups)
                    self.animation_player.create_particles('heal_left', player.rect.center, groups)

    def ball(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost

            status = ''

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
                status = '_left'
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
                status = '_up'
            else:
                direction = pygame.math.Vector2(0, 1)
                status = '_down'

            for i in range(1, 7):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    self.animation_player.create_particles(f'ball_{i}{status}', (player.rect.centerx + offset_x, player.rect.centery), groups)
                    self.animation_player.create_particles(f'ball_impulse{status}', (player.rect.centerx + offset_x, player.rect.centery), groups)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    self.animation_player.create_particles(f'ball_{i}{status}', (player.rect.centerx, player.rect.centery), groups)
                    self.animation_player.create_particles(f'ball_impulse{status}', (player.rect.centerx, player.rect.centery + offset_y), groups)

    def tentacles(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost

            status = ''

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
                status = '_left'
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)
                status = '_left'

            for i in range(1, 7):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles(f'tentacles{status}', (x, y), groups)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles(f'tentacles{status}', (x, y), groups)
