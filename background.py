from pico2d import *


class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(640, 360)

class Blacksmith:
    def __init__(self):
        self.image = load_image('Blacksmith.png')
        self.frame = 1
        self.w ,self.h = 288,170
        self.x, self.y = 200, 150
        self.last_time = get_time()
        self.frame_interval = 0.2

    def update(self):
        current_time = get_time()
        if current_time - self.last_time > self.frame_interval:
            self.frame += 1
            if self.frame > 4:
                self.frame = 1
            self.last_time = current_time

    def draw(self):
        self.image.clip_draw(self.frame * self.w, 610, self.w , self.h, self.x, self.y)


class Ground:
    def __init__(self):
        self.image = load_image('Tile_ground.png')
        self.tile_w = 32
        self.tile_h = 32
        self.tile_count = 1280//self.tile_w

    def update(self):
        pass

    def draw_tile(self, row, col, x, y):
        left = col * self.tile_w
        bottom = self.image.h - (row + 1) * self.tile_h
        self.image.clip_draw(left, bottom, self.tile_w, self.tile_h, x, y)

    def draw(self):
        for i in range(self.tile_count):

            x = i * self.tile_w + self.tile_w // 2

            y = self.tile_h * 0
            self.draw_tile(2, 1, x, y)

            y = self.tile_h * 1
            self.draw_tile(1, 1, x, y)

            y = self.tile_h * 2
            self.draw_tile(1, 1, x, y)

            y = self.tile_h * 3
            self.draw_tile(0, 1, x, y)