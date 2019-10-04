import pygame
from pygame.rect import Rect

from player import Player
from tile import Tile, TwoStatesTile
from utils import load_image


class Board:
    def __init__(self, width, height, field, toggle_rules):
        self.grass_image = load_image('images/grass.png')
        self.wall_image = load_image('images/box.png')
        self.door_image = load_image('images/door.png')
        self.door_opened_image = load_image('images/door_opened.png')
        self.toggle_image = load_image('images/toggle.png')
        self.toggle_pressed_image = load_image('images/toggle_activated.png')

        self.tiles_group = pygame.sprite.Group()
        self.walls_group = pygame.sprite.Group()
        self.doors_group = pygame.sprite.Group()

        self.width = width
        self.height = height
        self.field = [row.copy() for row in field]
        self.toggle_rules = toggle_rules

        self.grass = []
        self.walls = []
        self.doors = []
        self.toggles = [None] * len(toggle_rules)

        self.doors_opened = False

        for row in range(len(field)):
            for col in range(len(field[row])):
                if field[row][col] == 'f':
                    self.grass.append(Tile(self.grass_image, col, row, (self.tiles_group,), 50, 50))
                elif field[row][col] == 'w':
                    self.walls.append(Tile(self.wall_image, col, row, (self.walls_group, self.tiles_group), 50, 50))
                elif field[row][col] == 'd':
                    self.doors.append(TwoStatesTile([self.door_image, self.door_opened_image], col, row,
                                                    (self.doors_group, self.tiles_group), 50, 50))
                elif field[row][col].isdigit():
                    self.toggles[int(field[row][col]) - 1] = (
                        TwoStatesTile([self.toggle_image, self.toggle_pressed_image], col, row,
                                      (self.doors_group, self.tiles_group), 50, 50))

    def draw(self, screen, camera):
        self.update_draw_poses(camera)
        self.tiles_group.draw(screen)

    def update_draw_poses(self, camera):
        for tile in self.grass + self.walls + self.doors + self.toggles:
            tile.update_draw_pos(camera.dx, camera.dy)

    def can_move_player(self, player: Player, shift):
        pl_rect = player.rect
        new_rect = Rect(pl_rect.x + shift[0], pl_rect.y + shift[1] + 30, pl_rect.width, pl_rect.height - 30)

        if new_rect.collidelist(self.walls) != -1:
            return False
        if not self.doors_opened and new_rect.collidelist(self.doors) != -1:
            return False
        if new_rect.collidelist(self.toggles) != -1:
            return False

        return True

    def try_toggle(self, player):
        grow_on = 30
        pl_rect = player.rect
        new_rect = Rect(pl_rect.x - grow_on // 2, pl_rect.y - grow_on // 2, pl_rect.width + grow_on,
                        pl_rect.height + grow_on)

        toggle_id = new_rect.collidelist(self.toggles)
        if toggle_id != -1:
            self.toggles[toggle_id].change_state()
            for toggle_num in self.toggle_rules[toggle_id]:
                self.toggles[toggle_num].change_state()

        self.check_win()

    def check_win(self):
        if all(map(lambda x: x.activated, self.toggles)):
            self.doors_opened = True
        else:
            self.doors_opened = False
        self.update_doors_state()

    def update_doors_state(self):
        for door in self.doors:
            if door.activated != self.doors_opened:
                door.change_state()
