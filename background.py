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