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

        while running:
            self.screen.fill('Black')
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

