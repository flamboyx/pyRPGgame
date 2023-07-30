import pygame
from settings import *
from level import Level
from menu import Button

class Game:
    def __init__(self):
        pygame.init()
        self.running = True

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Delza")
        self.icon = pygame.image.load("images/icon.png").convert_alpha()
        pygame.display.set_icon(self.icon)

        self.level = Level()

        self.font = pygame.font.Font(UI_FONT, TITLE_FONT_SIZE)
        self.font_bg = pygame.font.Font(UI_FONT, TITLE_FONT_SIZE + 2)
        self.menu_bg = pygame.transform.scale_by(pygame.image.load("images/menu.png").convert_alpha(), 2 / 3)

    def run(self):
        while self.running:
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
                    elif event.key == pygame.K_m:
                        self.level.toggle_menu()

    def menu(self):
        menu = True

        title = self.font.render('Delza', False, UI_BORDER_COLOR)
        title_rect = title.get_rect(x = (WIDTH - title.get_width()) // 2, y = HEIGHT // 2 - 150)
        title_bg = self.font_bg.render('Delza', False, UI_BG_COLOR)
        title_bg_rect = title_bg.get_rect(x = (WIDTH - title.get_width()) // 2 + 2, y = HEIGHT // 2 - 150 + 2)


        play_button = Button((WIDTH - 480) // 2, HEIGHT // 2 + 100,
                             WIDTH // 4, HEIGHT // 16,
                             TEXT_COLOR, UI_BG_COLOR,
                             'Play', MENU_FONT_SIZE)


        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                menu = False

            self.screen.blit(self.menu_bg, (-100, 0))
            self.screen.blit(title_bg, title_bg_rect)
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.menu()
    while game.running:
        game.run()
