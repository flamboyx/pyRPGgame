import time

import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('images/player.jpg').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.jump = False
        self.jump_count = 30

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.jump:
            if keys[pygame.K_w]:
                self.jump = True
                self.speed = 12
        else:
            if self.jump_count >= -30:
                if self.jump_count > 0:
                    self.direction.y = -self.jump_count ** 2
                    self.speed -= 0.2
                else:
                    self.direction.y = self.jump_count ** 2
                    self.speed += 0.2
                self.jump_count -= 1
            else:
                self.jump = False
                self.jump_count = 30
                self.speed = 6

        if keys[pygame.K_d]:
            self.direction.x = 10
        elif keys[pygame.K_a]:
            self.direction.x = -10
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')

    def collision(self, direction):
        obstacleabove = False

        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        if not obstacleabove:
                            self.rect.bottom = sprite.rect.top
                        else:
                            self.direction.y = 24


                    if self.direction.y < 0:
                        self.jump = False
                        self.direction.y = self.jump_count ** 2
                        obstacleabove = True
                        self.rect.top = sprite.rect.bottom
                else:
                    self.direction.y = 12


    def update(self):
        self.input()
        self.move(self.speed)