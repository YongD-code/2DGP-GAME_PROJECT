from pico2d import *

CROP_TYPE = {
    "corn": 0,
    "pumpkin": 1,
    "potato": 2,
    "strawberry": 3
}

class Crop:
    def __init__(self,x,y,crop_type="corn"):
        self.image = load_image('crop.png')
        self.x,self.y = x,y
        self.stage = 4
        self.max_stage = 1
        self.timer = 0
        self.harvested = False
        self.crop_type = crop_type

    def harvest(self):
        self.harvested = True

    def update(self,frame_time):
        self.timer += frame_time
        if self.timer > 1.0 and self.stage > self.max_stage:
            self.stage -= 1
            self.timer = 0

    def draw(self):
        if not self.harvested:
            row = CROP_TYPE[self.crop_type]
            sy = row * 16

            if self.stage >= 3:
                self.image.clip_draw(self.stage * 16, sy, 16, 16, self.x, self.y+10, 32, 32)
            else:
                self.image.clip_draw(self.stage * 16, sy, 16, 16, self.x, 132, 48, 48)
