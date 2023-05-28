import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.status.split('_')[0]

        # graphic
        full_path = f'images/weapons/{player.weapon}/{direction}.png'
        if player.weapon == 'sword':
            if direction == 'right' or direction == 'left':
                self.image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (64, 16))
            elif direction == 'down' or direction == 'up':
                self.image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (16, 64))
        elif player.weapon == 'scythe':
            if direction == 'right' or direction == 'left':
                self.image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (74, 48))
            elif direction == 'down' or direction == 'up':
                self.image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (48, 74))
        elif player.weapon == 'spear':
            if direction == 'right' or direction == 'left':
                self.image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (100, 28))
            elif direction == 'down' or direction == 'up':
                self.image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (28, 100))
        elif player.weapon == 'heavysword':
            if direction == 'right' or direction == 'left':
                self.image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (92, 32))
            elif direction == 'down' or direction == 'up':
                self.image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (32, 92))

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-92, 0))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(92, 0))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0, -96))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0, 96))
