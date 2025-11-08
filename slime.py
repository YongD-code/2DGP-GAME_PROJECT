from pico2d import *
import math

class Slime:
    DETECT_RADIUS   = 260.0
    STOP_DIST       = 24.0
    IDLE_FRAME_TIME = 0.15
    MOVE_FRAME_TIME = 0.10
    MOVE_SPEED      = 110.0

    def __init__(self, x, y, color='blue'):
        self.blue_slime  = load_image('blue_slime.png')
        self.green_slime = load_image('green_slime.png')
        self.red_slime   = load_image('red_slime.png')

        self.cols = 7
        self.rows = 6
        self.w = 128 // self.cols
        self.h = 20

        self.x, self.y = x, y
        self.dir = -1
        self.speed = Slime.MOVE_SPEED
        self.frame = 0
        self.action = 0
        self.time_acc = 0.0

        self.idle_row = 6
        self.idle_frame_count = 4
        self.move_row = 5
        self.move_frame_count = 5

        self.sheet = None
        self.set_color(color)

    def set_color(self, color: str):
        c = (color or '').lower()
        if c == 'green':
            self.sheet = self.green_slime
        elif c == 'red':
            self.sheet = self.red_slime
        else:
            self.sheet = self.blue_slime

    def update(self, frame_time):
        try:
            from world import player, left_boundary, right_boundary
        except ImportError:
            player = None
            left_boundary, right_boundary = 0, 999999

        if player is not None:
            same_floor = abs(player.y - self.y) <= 100
            if same_floor:
                dx = player.x - self.x
                if abs(dx) <= Slime.DETECT_RADIUS:
                    self.action = 1
                    if abs(dx) > Slime.STOP_DIST:
                        self.dir = 1 if dx > 0 else -1
                        self.x += self.dir * self.speed * frame_time
                else:
                    self.action = 0
            else:
                self.action = 0
        else:
            self.action = 0

        if self.x < left_boundary + 40:
            self.x = left_boundary + 40
            self.dir = 1
        elif self.x > right_boundary - 40:
            self.x = right_boundary - 40
            self.dir = -1

        self.time_acc += frame_time
        if self.action == 0:
            if self.time_acc >= Slime.IDLE_FRAME_TIME:
                self.frame = (self.frame + 1) % self.idle_frame_count
                self.time_acc = 0.0
        else:
            if self.time_acc >= Slime.MOVE_FRAME_TIME:
                self.frame = (self.frame + 1) % self.move_frame_count
                self.time_acc = 0.0

    def draw(self):
        if self.action == 0:
            row = self.idle_row
            frame_count = self.idle_frame_count
        else:
            row = self.move_row
            frame_count = self.move_frame_count

        idx = int(self.frame) % frame_count
        x_clip = idx * self.w
        y_clip = (self.rows + row) * self.h

        draw_w = self.w * 3
        draw_h = self.h * 3

        if self.dir == 1:
            self.sheet.clip_draw(x_clip, y_clip, self.w, self.h,self.x, self.y, draw_w, draw_h)
        else:
            self.sheet.clip_composite_draw(x_clip, y_clip, self.w, self.h, 0, 'h', self.x, self.y, draw_w, draw_h)
