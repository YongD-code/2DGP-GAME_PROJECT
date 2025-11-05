from pico2d import *

class Slime:
    def __init__(self, x, y):
        self.image_right = load_image('blue_slime.png')
        #self.image_left = load_image('blue_slime_R.png')

        self.cols = 7
        self.rows = 6
        self.w = 128 // self.cols
        self.h = 170 // self.rows


        self.x, self.y = x, y
        self.dir = -1
        self.speed = 50
        self.frame = 0
        self.action = 0
        self.time_acc = 0.0

    def update(self, frame_time):
        self.time_acc += frame_time
        if self.time_acc > 0.15:
            self.frame = (self.frame + 1) % self.cols
            self.time_acc = 0.0

        self.x += self.dir * self.speed * frame_time

        from world import left_boundary, right_boundary
        if self.x < left_boundary + 40:
            self.x = left_boundary + 40
            self.dir = 1
        elif self.x > right_boundary - 40:
            self.x = right_boundary - 40
            self.dir = -1

    def draw(self):
        row = 0

        x_clip = int(self.frame) * self.w
        y_clip = (self.rows - 1 - row) * self.h

        img = self.image_right if self.dir == 1 else self.dir == -1 and self.image_right

        if self.dir == 1:
            img.clip_draw(x_clip, y_clip,self.w, self.h,self.x, self.y,self.w, self.h)
        else:
            img.clip_composite_draw(x_clip, y_clip,self.w, self.h,0, 'h',self.x, self.y, self.w*2, self.h*2)
