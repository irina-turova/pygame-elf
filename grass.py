from tile import Tile
from utils import load_image


class GrassTile(Tile):
    def __init__(self, pos_x, pos_y, groups):
        super().__init__(load_image('images/grass.png'), pos_x, pos_y, groups)