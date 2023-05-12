import pygame
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("My Game")
        self.icon = pygame.image.load("images/icon.png").convert_alpha()
        pygame.display.set_icon(self.icon)
        self.level = Level()

    def run(self):
        running = True
        fullscreenmode = True

        bg = pygame.image.load("images/backgrounds/grass.png").convert_alpha()
        player = pygame.image.load('images/player.jpg').convert_alpha()

        bg_x = 0
        bg_y = 0

        bg_speed = 10

        while running:
            self.screen.blit(bg, (bg_x, bg_y))
            self.screen.blit(bg, (bg_x + 1920, bg_y))
            self.screen.blit(bg, (bg_x - 1920, bg_y))
            self.screen.blit(bg, (bg_x, bg_y + 1080))
            self.screen.blit(bg, (bg_x, bg_y - 1080))
            self.screen.blit(bg, (bg_x + 1920, bg_y + 1080))
            self.screen.blit(bg, (bg_x - 1920, bg_y + 1080))
            self.screen.blit(bg, (bg_x + 1920, bg_y - 1080))
            self.screen.blit(bg, (bg_x - 1920, bg_y - 1080))

            if bg_x == 1920 or bg_x == -1920:
                bg_x = 0
            elif bg_y == 1080 or bg_y == -1080:
                bg_y = 0

            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                    if event.key == pygame.K_RETURN and pygame.key.get_mods() and pygame.KMOD_RALT:
                        if fullscreenmode:
                            screen = pygame.display.set_mode((WIDTH // 2, HEIGHT // 2), pygame.RESIZABLE)
                            fullscreenmode = False
                        else:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                            fullscreenmode = True


if __name__ == '__main__':
    game = Game()
    game.run()

