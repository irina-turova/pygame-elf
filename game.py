import sys

import pygame

from board import Board
from camera import Camera
from player import Player
from utils import load_image


class Game:
    tile_width = 50
    tile_height = 50

    def __init__(self, screen_width, screen_height, fps, levels):

        self.fps = fps
        self.step = 10
        self.levels = levels[:]
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.player_group = pygame.sprite.Group()

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.running = False

        self.player = None
        self.board = None
        self.camera = Camera(screen_width, screen_height)

        self.start_screen()
        if levels:
            self.current_level = 0
            self.load_level(levels[0])

    def load_level(self, level_file):
        self.player_group = pygame.sprite.Group()

        fin = open(level_file)

        width, height = map(int, fin.readline().split())
        player_pos_x, player_pos_y = map(int, fin.readline().split())

        self.player = Player(player_pos_x, player_pos_y, (self.player_group,), 50, 50)

        cnt_toggles = int(fin.readline())
        toggles = [list(map(lambda x: int(x) - 1, fin.readline().split())) for _ in range(cnt_toggles)]
        field = [list(line.strip()) for line in fin.readlines()]

        self.board = Board(width, height, field, toggles)
        self.camera.set_field_size(width * self.tile_width, height * self.tile_height)
        self.camera.update(self.player.current_x, self.player.current_y, self.player.current_x, self.player.current_y)

    def start_screen(self):
        intro_text = ['Помогите маленькому эльфу найти путь домой.',
                      'Активируйте все рычаги,',
                      'чтобы выбраться из', 'комнаты.',
                      'Для активации рычага', 'используйте ПРОБЕЛ']

        fon = pygame.transform.scale(load_image('images/bg.jpg'), (self.screen_width, self.screen_height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.SysFont("comicsansms", 22)
        text_coord = 30
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 20
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.fps)

    def start(self):
        self.running = True
        self.run()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    shift = [0, 0]
                    action = False
                    if event.key == pygame.K_LEFT:
                        shift[0] -= self.step
                    if event.key == pygame.K_RIGHT:
                        shift[0] += self.step
                    if event.key == pygame.K_UP:
                        shift[1] -= self.step
                    if event.key == pygame.K_DOWN:
                        shift[1] += self.step
                    if event.key == pygame.K_SPACE:
                        action = True

                    if action:
                        self.board.try_toggle(self.player)
                    if self.board.can_move_player(self.player, shift):
                        self.player.shift(*shift)
                    self.camera.update(*shift, self.player.current_x, self.player.current_y)

                    if self.player_outside_field():
                        self.load_next_level()

            self.screen.fill(pygame.Color(0, 0, 0))
            self.board.draw(self.screen, self.camera)
            self.draw_player()

            pygame.display.flip()

            self.clock.tick(self.fps)

    def draw_player(self):
        self.player.update_draw_pos(self.camera.dx, self.camera.dy)
        self.player_group.draw(self.screen)

    def player_outside_field(self):
        x = self.player.current_x + self.player.width // 2
        y = self.player.current_y + self.player.height // 2
        return x <= 0 or (self.board.width * self.tile_width) <= x or y <= 0 or (self.board.height * self.tile_height) <= y

    def load_next_level(self):
        self.current_level += 1
        if self.current_level >= len(self.levels):
            self.terminate()
        else:
            self.load_level(self.levels[self.current_level])
