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
UPGRADE_BG_COLOR_SELECTED = '#FFD073'
UI_BORDER_COLOR = '#2A5234'
TEXT_COLOR = '#DED4AD'
TEXT_COLOR_SELECTED = 'black'

HEALTH_COLOR = '#AB0000'
ENERGY_COLOR = '#FFFF3B'
UI_BORDER_COLOR_ACTIVE = '#E6FFE6'

BAR_COLOR = '#FFBF40'
BAR_COLOR_SELECTED = '#FFAA00'


weapon_data = {
    'sword': {'cooldown': 100, 'damage': 20, 'graphic': 'images/weapons/sword/up.png'},
    'scythe': {'cooldown': 150, 'damage': 30, 'graphic': 'images/weapons/scythe/up.png'},
    'spear': {'cooldown': 115, 'damage': 24, 'graphic': 'images/weapons/spear/up.png'},
    'heavysword': {'cooldown': 300, 'damage': 40, 'graphic': 'images/weapons/heavysword/up.png'}}

magic_data = {
    'ball': {'strength': 20, 'cost': 25, 'graphic': 'images/spells/ball.png'},
    'heal': {'strength': 20, 'cost': 15, 'graphic': 'images/spells/heal.png'},
    'tentacles': {'strength': 15, 'cost': 20, 'graphic': 'images/spells/tentacles.png'}}

enemy_data = {
    'bat': {'health': 100, 'exp': 100, 'damage': 10, 'attack_cooldown': 300, 'attack_type': 'dark_eye',
            'attack sound': None, 'speed': 5, 'resistance': 5, 'attack_radius': 40, 'notice_radius': 480},
    'jaws': {'health': 200, 'exp': 150, 'damage': 30, 'attack_cooldown': 900, 'attack_type': 'bite',
             'attack sound': None, 'speed': 2, 'resistance': 2, 'attack_radius': 70, 'notice_radius': 340},
    'poo': {'health': 150, 'exp': 200, 'damage': 40, 'attack_cooldown': 700, 'attack_type': 'goo',
            'attack sound': None, 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 420}}
