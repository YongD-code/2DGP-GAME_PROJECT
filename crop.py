from pico2d import *

class Crop:
    def __init__(self,x,y):
        self.image = load_image('crop.png')
        self.x,self.y = x,y
        self.stage = 0
        self.max_stage = 3
        self.timer = 0

    def update(self,frame_time):
        self.timer += frame_time
        if self.timer > 5.0 and self.stage < self.max_stage:
            self.stage += 1
            self.timer = 0

    def draw(self):
        self.image.clip_draw(self.stage * 32, 0, 32, 32, self.x, self.y, 64, 64)