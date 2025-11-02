from pico2d import *

class Crop:
    def __init__(self,x,y):
        self.image = load_image('crop.png')
        self.x,self.y = x,y
        self.stage = 4
        self.max_stage = 1
        self.timer = 0
        self.harvested = False

    def harvest(self):
        self.harvested = True

    def update(self,frame_time):
        self.timer += frame_time
        if self.timer > 6.0 and self.stage > self.max_stage:
            self.stage -= 1
            self.timer = 0

    def draw(self):
        if not self.harvested:
            if self.stage >= 3:
                self.image.clip_draw(self.stage * 16, 0, 16, 16, self.x, self.y+10, 32, 32)
            else:
                self.image.clip_draw(self.stage * 16, 0, 16, 16, self.x, 132, 48, 48)
