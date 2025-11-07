from pico2d import *

class Slime:
    def __init__(self, x, y):
        self.blue_slime = load_image('blue_slime.png')
        self.green_slime = load_image('green_slime.png')
        self.red_slime = load_image('red_slime.png')

        self.cols = 7
        self.rows = 6
        self.w = 128 // self.cols
        self.h = 20

        self.x, self.y = x, y
        self.dir = -1
        self.speed = 50
        self.frame = 0
        self.action = 0
        self.time_acc = 0.0

        self.idle_frame_count = 4
        self.idle_row = 6

    def update(self, frame_time):
        self.time_acc += frame_time
        if self.time_acc > 0.15:
            if self.action == 0:
                self.frame = (self.frame + 1) % self.idle_frame_count
            else:
                self.frame = (self.frame + 1) % self.cols
            self.time_acc = 0.0

        self.action = 0

        from world import left_boundary, right_boundary
        if self.x < left_boundary + 40:
            self.x = left_boundary + 40
            self.dir = 1
        elif self.x > right_boundary - 40:
            self.x = right_boundary - 40
            self.dir = -1

    def draw(self):
        row = 6

        x_clip = int(self.frame) * self.w
        y_clip = (self.rows + row) * self.h

        img = self.blue_slime if self.dir == 1 else self.dir == -1 and self.blue_slime

        if self.dir == 1:
            img.clip_draw(x_clip, y_clip,self.w, self.h,self.x, self.y,self.w, self.h)
        else:
            img.clip_composite_draw(x_clip, y_clip,self.w, self.h,0, 'h',self.x, self.y, self.w*3, self.h*3)
