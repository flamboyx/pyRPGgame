import pygame
from settings import *
from level import Level
from menu import Button


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.main_menu = True
        self.settings = False

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Delza")
        self.icon = pygame.image.load("images/icon.png").convert_alpha()
        pygame.display.set_icon(self.icon)

        self.level = Level()

        self.font = pygame.font.Font(UI_FONT, TITLE_FONT_SIZE)
        self.font_bg = pygame.font.Font(UI_FONT, TITLE_FONT_SIZE + 2)
        scale_x = 3840.0 // WIDTH
        self.menu_bg = pygame.transform.scale_by(pygame.image.load("images/menu.png").convert_alpha(), scale_x / 3)

    def run(self):
        while self.running:
            self.screen.fill('Black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                    elif event.key == pygame.K_m:
                        self.level.toggle_menu()

    def menu(self):
        title = self.font.render('Delza', False, UI_BORDER_COLOR)
        title_rect = title.get_rect(x=(WIDTH - title.get_width()) // 2, y=HEIGHT // 2 - HEIGHT // 8)
        title_bg = self.font_bg.render('Delza', False, UI_BG_COLOR)
        title_bg_rect = title_bg.get_rect(x=(WIDTH - title.get_width()) // 2 + 2, y=HEIGHT // 2 - HEIGHT // 8 + 2)

        play_button_y = HEIGHT // 2 + HEIGHT // 10

        while title_bg_rect.y + title_bg.get_height() >= play_button_y:
            play_button_y += HEIGHT // 50

        play_button = Button((WIDTH - WIDTH // 4) // 2, play_button_y,
                             WIDTH // 4, HEIGHT // 16,
                             TEXT_COLOR, UI_BG_COLOR,
                             'Play', MENU_FONT_SIZE)

        settings_button = Button((WIDTH - WIDTH // 4) // 2, play_button_y + play_button.height * 3 // 2,
                                 WIDTH // 4, HEIGHT // 16,
                                 TEXT_COLOR, UI_BG_COLOR,
                                 'Settings', MENU_FONT_SIZE)

        back_button = Button((WIDTH - WIDTH // 4) // 2, play_button_y + play_button.height * 3 // 2,
                             WIDTH // 4, HEIGHT // 16,
                             TEXT_COLOR, UI_BG_COLOR,
                             'Back', MENU_FONT_SIZE)

        screen_resolution = Button((WIDTH - WIDTH // 4) // 2, play_button_y,
                                   WIDTH // 4, HEIGHT // 16,
                                   TEXT_COLOR, UI_BG_COLOR,
                                   'Screen Resolution', MENU_FONT_SIZE)

        while self.main_menu:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_menu = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                elif play_button.is_pressed(mouse_pos, mouse_pressed):
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.main_menu = False
                        self.running = True
                elif settings_button.is_pressed(mouse_pos, mouse_pressed):
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.main_menu = False
                        self.settings = True

            self.screen.blit(self.menu_bg, (-WIDTH // 20, HEIGHT - self.menu_bg.get_height() + HEIGHT // 10))
            self.screen.blit(title_bg, title_bg_rect)
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(settings_button.image, settings_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

        while self.settings:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.settings = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu = True
                        self.settings = False
                elif back_button.is_pressed(mouse_pos, mouse_pressed):
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.main_menu = True
                        self.settings = False

            self.screen.blit(self.menu_bg, (-WIDTH // 20, HEIGHT - self.menu_bg.get_height() + HEIGHT // 10))
            self.screen.blit(screen_resolution.image, screen_resolution.rect)
            self.screen.blit(back_button.image, back_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    while game.main_menu:
        game.menu()
    while game.running:
        game.run()
