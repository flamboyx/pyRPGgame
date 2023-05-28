import pygame

pygame.init()

screen = pygame.display.Info()

WIDTH = screen.current_w
HEIGHT = screen.current_h
FPS = 60
TILESIZE = 64

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'images/weapons/sword/up.png'},
    'scythe': {'cooldown': 100, 'damage': 15, 'graphic': 'images/weapons/scythe/up.png'},
    'spear': {'cooldown': 100, 'damage': 15, 'graphic': 'images/weapons/spear/up.png'},
    'heavysword': {'cooldown': 100, 'damage': 15, 'graphic': 'images/weapons/heavysword/up.png'},
}
