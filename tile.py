import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, images, pos_x, pos_y, groups, tile_width, tile_height):
        super().__init__(*groups)
        self.current_x = pos_x * tile_width
        self.current_y = pos_y * tile_height
        self.width = tile_width
        self.height = tile_height

        if type(images) is not list:
            images = [images]

        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect().move(self.current_x, self.current_y)

    def shift(self, dx, dy):
        self.current_x += dx
        self.current_y += dy

    def update_draw_pos(self, cam_x, cam_y):
        self.rect.x = self.current_x - cam_x
        self.rect.y = self.current_y - cam_y


class TwoStatesTile(Tile):
    def __init__(self, images, pos_x, pos_y, groups, tile_width, tile_height):
        super().__init__(images, pos_x, pos_y, groups, tile_width, tile_height)

        self.activated = False

    def change_state(self):
        self.activated = not self.activated
        self.image = self.images[self.activated]
