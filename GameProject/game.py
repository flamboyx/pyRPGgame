import pygame
from settings import *
from level import Level
from player import Player
from menu import Button


class Game:
    def __init__(self):
        pygame.init()

        self.running = True
        self.main_menu = True
        self.settings = False
        self.game = False
        self.game_over = False
        self.win = False

        self.start_time = 0
        self.end_time = 0

        with open('saves/records.txt') as f:
            self.record = min([float(t) for t in f])
        f.close()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Delza")
        self.icon = pygame.image.load("images/icon.png").convert_alpha()
        pygame.display.set_icon(self.icon)

        self.font = pygame.font.Font(UI_FONT, TITLE_FONT_SIZE)
        self.font_bg = pygame.font.Font(UI_FONT, TITLE_FONT_SIZE + 2)
        self.menu_font = pygame.font.Font(UI_FONT, MENU_FONT_SIZE)
        scale_x = 3840.0 // WIDTH
        self.menu_bg = pygame.transform.scale_by(pygame.image.load("images/menu.png").convert_alpha(), scale_x / 3)

    def run(self):
        self.level = Level()
        self.start_time = pygame.time.get_ticks() / 1000

        while self.game:
            self.screen.fill('Black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

            if self.level.game_over:
                self.game_over_screen()

            if self.level.win:
                self.win_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game = False
                        self.running = False
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
                        self.main_menu = False
                        self.running = False
                elif play_button.is_pressed(mouse_pos, mouse_pressed):
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.main_menu = False
                        self.game = True
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

    def game_over_screen(self):
        message = self.font.render('Game Over', False, UI_BORDER_COLOR)
        message_rect = message.get_rect(x=(WIDTH - message.get_width()) // 2, y=HEIGHT // 2 - message.get_height())
        message_bg = self.font_bg.render('Game Over', False, UI_BG_COLOR)
        message_bg_rect = message_bg.get_rect(x=(WIDTH - message.get_width()) // 2 + 2,
                                              y=HEIGHT // 2 - message.get_height() + 2)

        play_again_button_y = HEIGHT // 2 - message_bg.get_height()

        while message_bg_rect.y + message_bg.get_height() >= play_again_button_y:
            play_again_button_y += HEIGHT // 50

        play_again_button = Button((WIDTH - WIDTH // 4) // 2, play_again_button_y,
                                   WIDTH // 4, HEIGHT // 16,
                                   TEXT_COLOR, UI_BG_COLOR,
                                   'Try Again', MENU_FONT_SIZE)

        menu_button = Button((WIDTH - WIDTH // 4) // 2, play_again_button_y + play_again_button.height * 3 // 2,
                             WIDTH // 4, HEIGHT // 16,
                             TEXT_COLOR, UI_BG_COLOR,
                             'Main Menu', MENU_FONT_SIZE)

        self.game_over = True
        self.game = False
        del self.level.player

        while self.game_over:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_over = False
                        self.main_menu = True
                        del self.level
                elif play_again_button.is_pressed(mouse_pos, mouse_pressed):
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.game_over = False
                        self.game = True
                        del self.level
                        self.level = Level()
                elif menu_button.is_pressed(mouse_pos, mouse_pressed):
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.game_over = False
                        self.main_menu = True
                        del self.level

            self.screen.blit(message_bg, message_bg_rect)
            self.screen.blit(message, message_rect)
            self.screen.blit(play_again_button.image, play_again_button.rect)
            self.screen.blit(menu_button.image, menu_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def win_screen(self):
        self.end_time = pygame.time.get_ticks() / 1000

        win_time = self.end_time - self.start_time

        color = TEXT_COLOR

        if self.record > win_time:
            self.record = win_time
            color = BAR_COLOR_SELECTED
            with open('saves/records.txt', 'a') as f:
                print(self.record, file=f)
            f.close()

        h = ''
        m = ''
        bh = ''
        bm = ''

        if win_time >= 60 * 60:
            hours = win_time // 3600
            win_time %= 3600

            if hours > 9:
                h = str(hours) + 'h:'
            else:
                h = '0' + str(hours) + 'h:'
        if win_time >= 60:
            mins = win_time // 60
            win_time %= 60

            if mins > 9:
                m = str(mins) + 'm:'
            else:
                m = '0' + str(mins) + 'm:'

        if win_time != self.record:
            if self.record >= 60 * 60:
                hours = self.record // 3600
                self.record %= 3600

                if hours > 9:
                    bh = str(hours) + 'h:'
                else:
                    bh = '0' + str(hours) + 'h:'
            if self.record >= 60:
                mins = self.record // 60
                self.record %= 60

                if mins > 9:
                    bm = str(mins) + 'm:'
                else:
                    bm = '0' + str(mins) + 'm:'

        win_time = round(win_time, 3)
        best_win_time = round(self.record, 3)

        message = self.font.render('You Win!', False, UI_BORDER_COLOR)
        message_rect = message.get_rect(x=(WIDTH - message.get_width()) // 2,
                                        y=HEIGHT // 2 - message.get_height())
        message_bg = self.font_bg.render('You Win!', False, UI_BG_COLOR)
        message_bg_rect = message_bg.get_rect(x=(WIDTH - message.get_width()) // 2 + 2,
                                              y=HEIGHT // 2 - message.get_height() + 2)

        time = self.menu_font.render('Your Time:', False, TEXT_COLOR)
        time_rect = time.get_rect(x=(WIDTH - message.get_width()) // 2, y=HEIGHT // 2)

        your_time = self.menu_font.render(h + m + str(win_time) + 's', False, TEXT_COLOR)
        your_time_rect = your_time.get_rect(x=(WIDTH - message.get_width()) // 2 + time.get_width(),
                                            y=HEIGHT // 2)

        best_time = self.menu_font.render('Best Time:', False, TEXT_COLOR)
        best_time_rect = best_time.get_rect(x=(WIDTH - message.get_width()) // 2,
                                            y=HEIGHT // 2 + time.get_height())

        your_best_time = self.menu_font.render(bh + bm + str(best_win_time) + 's', False, color)
        your_best_time_rect = your_best_time.get_rect(x=(WIDTH - message.get_width()) // 2 + best_time.get_width(),
                                                      y=HEIGHT // 2 + time.get_height())

        menu_button_y = HEIGHT // 2 + time.get_height()

        while your_best_time_rect.y + best_time.get_height() >= menu_button_y:
            menu_button_y += HEIGHT // 50

        menu_button = Button((WIDTH - WIDTH // 4) // 2, menu_button_y,
                             WIDTH // 4, HEIGHT // 16,
                             TEXT_COLOR, UI_BG_COLOR,
                             'Main Menu', MENU_FONT_SIZE)

        self.win = True
        self.game = False

        while self.win:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.win = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.win = False
                        self.main_menu = True
                        del self.level
                elif menu_button.is_pressed(mouse_pos, mouse_pressed):
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.win = False
                        self.main_menu = True
                        del self.level

            self.screen.blit(message_bg, message_bg_rect)
            self.screen.blit(message, message_rect)
            self.screen.blit(time, time_rect)
            self.screen.blit(your_time, your_time_rect)
            self.screen.blit(best_time, best_time_rect)
            self.screen.blit(your_best_time, your_best_time_rect)
            self.screen.blit(menu_button.image, menu_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    while game.running:
        while game.main_menu:
            game.menu()
        while game.game:
            game.run()
        while game.game_over:
            game.game_over_screen()
        while game.win:
            game.win_screen()
