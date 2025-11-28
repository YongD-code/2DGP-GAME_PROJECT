from pico2d import *

import game_framework
FPS_IDLE = 6

class Idle:
    def __init__(self, player):
        self.player = player
        self.image_right = load_image('_Idle.png')
        self.image_left = load_image('_Idle_R.png')
        self.image = self.image_right
        self.frame = 0

    def enter(self,event):
        if self.player.dir == 1:
            self.image = self.image_right
        elif self.player.dir == -1:
            self.image = self.image_left

    def exit(self,event):
        pass

    def do(self):
        self.frame += FPS_IDLE * game_framework.frame_time

    def draw(self):
        frame = int(self.frame % 4)
        self.image.clip_draw(frame * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 3,self.player.h * 3)