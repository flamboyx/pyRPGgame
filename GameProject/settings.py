import pygame

pygame.init()

screen = pygame.display.Info()

WIDTH = screen.current_w
HEIGHT = screen.current_h
FPS = 60
TILESIZE = 64

HEALTH_BAR_HEIGHT = 30
ENERGY_BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 400
ENERGY_BAR_WIDTH = 300
ITEM_BOX_SIZE = 105
UI_FONT = 'images/fonts/DotGothic16-Regular.ttf'
UI_FONT_SIZE = 24

UI_BG_COLOR = '#3B2608'
UI_BORDER_COLOR = '#2A5234'
TEXT_COLOR = '#DED4AD'

HEALTH_COLOR = '#AB0000'
ENERGY_COLOR = '#FFFF3B'
UI_BORDER_COLOR_ACTIVE = '#E6FFE6'

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 20, 'graphic': 'images/weapons/sword/up.png'},
    'scythe': {'cooldown': 150, 'damage': 30, 'graphic': 'images/weapons/scythe/up.png'},
    'spear': {'cooldown': 115, 'damage': 24, 'graphic': 'images/weapons/spear/up.png'},
    'heavysword': {'cooldown': 300, 'damage': 40, 'graphic': 'images/weapons/heavysword/up.png'}}

magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': 'images/test.jpg'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': 'images/icon.png'}}

enemy_data = {
    'bat': {'health': 100, 'exp': 100, 'damage': 10, 'attack_cooldown': 300, 'attack_type': None,
            'attack sound': None, 'speed': 5, 'resistance': 5, 'attack_radius': 40, 'notice_radius': 480},
    'jaws': {'health': 200, 'exp': 150, 'damage': 30, 'attack_cooldown': 500, 'attack_type': None,
             'attack sound': None, 'speed': 2, 'resistance': 2, 'attack_radius': 70, 'notice_radius': 340}
}
