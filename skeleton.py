from pico2d import *

SKELETON_BW   = 26.0
SKELETON_BH   = 40.0
SKELETON_BX = 0.0
SKELETON_BY = 0.0

class Skeleton:

    DETECT_RADIUS   = 260.0
    STOP_DIST       = 24.0
    IDLE_FRAME_TIME = 0.15
    MOVE_FRAME_TIME = 0.10
    MOVE_SPEED      = 110.0

    def __init__(self,x,y):
        self.image = load_image('skeleton.png')
        self.cols = 7
        self.rows = 6
        self.w = 18
        self.h = 17

        self.x, self.y = x, y
        self.dir = -1
        self.speed = Skeleton.MOVE_SPEED
        self.frame = 0
        self.action = 0
        self.time_acc = 0.0

        self.idle_row = 6
        self.idle_frame_count = 4
        self.move_row = 5
        self.move_frame_count = 4

    def update(self, frame_time):
        try:
            from world import player, left_boundary, right_boundary
        except ImportError:
            player = None
            left_boundary, right_boundary = 0, 999999

        if player is not None:
            same_floor = abs(player.y - self.y - 80) <= 5
            if same_floor:
                dx = player.x - self.x
                if abs(dx) <= Skeleton.DETECT_RADIUS:
                    self.action = 1
                    if abs(dx) > Skeleton.STOP_DIST:
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
            if self.time_acc >= Skeleton.IDLE_FRAME_TIME:
                self.frame = (self.frame + 1) % self.idle_frame_count
                self.time_acc = 0.0
        else:
            if self.time_acc >= Skeleton.MOVE_FRAME_TIME:
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
        y_clip = row * self.h

        draw_w = self.w * 3
        draw_h = self.h * 3

        if self.dir == 1:
            self.image.clip_draw(x_clip, y_clip, self.w, self.h,self.x, self.y, draw_w*2, draw_h*2)
        else:
            self.image.clip_composite_draw(x_clip, y_clip, self.w, self.h, 0, 'h', self.x, self.y, draw_w*2, draw_h*2)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        cx = self.x + SKELETON_BX
        cy = self.y + SKELETON_BY
        return cx - SKELETON_BW, cy - SKELETON_BH , cx + SKELETON_BW, cy + SKELETON_BH

    def handle_collision(self, group, other):
        return