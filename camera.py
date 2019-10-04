class Camera:
    def __init__(self, screen_width, screen_height):
        self.dx = 0
        self.dy = 0
        self.field_width = None
        self.field_height = None
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, shift_x, shift_y, player_x, player_y):
        # print(self.field_width, self.field_height, self.screen_width, self.screen_height)
        if shift_x > 0 and player_x >= self.dx + self.screen_width // 2 or \
                shift_x < 0 and player_x <= self.dx + self.screen_width // 2:
            if 0 <= self.dx + shift_x <= self.field_width - self.screen_width:
                self.dx += shift_x
        if shift_y > 0 and player_y >= self.dy + self.screen_height // 2 or \
                shift_y < 0 and player_y <= self.dy + self.screen_height // 2:
            if 0 <= self.dy + shift_y <= self.field_width - self.screen_height:
                self.dy += shift_y

    def set_field_size(self, field_width, field_height):
        self.field_width, self.field_height = field_width, field_height
