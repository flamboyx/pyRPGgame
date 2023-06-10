import pygame
import pygame.locals
from settings import *

pygame.init()
screen = pygame.display.set_mode((300, 300))
# one image -> 7 subsurfaces
sheet = pygame.image.load('images/characters/main_character/up_attack/up_attack.png').convert_alpha()
imgs = []
for x in range(2):
    for y in range(2):
        imgs.append(sheet.subsurface((y * 64, x * 64, 64, 64)))
current_img = 0
# clock - FPS
clock = pygame.time.Clock()
# mainloop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    current_img = (current_img + 1) % (2 * 2)
    screen.fill((0, 0, 0))
    screen.blit(imgs[current_img], (150 - 16, 150 - 16))
    pygame.display.flip()
    clock.tick(12)
# save subsurfaces as separated images
for x in range(2 * 2):
    pygame.image.save(imgs[x], 'images/characters/main_character/up_attack/up_attack_' + str(x) + '.png')
    # name = 'flora_' + str(x) + '.png'
    # if int(x) < 10:
    #     pygame.image.save(imgs[x], 'images/graphics/flora/flora_00' + str(x) + '.png')
    # elif int(x) < 100:
    #     pygame.image.save(imgs[x], 'images/graphics/flora/flora_0' + str(x) + '.png')
    # elif int(x) < 1000:
    #     pygame.image.save(imgs[x], 'images/graphics/flora/flora_' + str(x) + '.png')
    # print(name, 'saved')
# the end
pygame.quit()
