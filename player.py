from tile import Tile
from utils import load_image


class Player(Tile):
    def __init__(self, pos_x, pos_y, groups, tile_width, tile_height):
        images = [load_image('images/char_front.png'), load_image('images/char_back.png'), load_image('images/char_left.png'), load_image('images/char_right.png')]
        super().__init__(images, pos_x, pos_y, groups, tile_width, tile_height)

    def shift(self, dx, dy):
        super().shift(dx, dy)
        if dx > 0:
            self.image = self.images[3]
        elif dx < 0:
            self.image = self.images[2]
        elif dy < 0:
            self.image = self.images[1]
        else:
            self.image = self.images[0]




