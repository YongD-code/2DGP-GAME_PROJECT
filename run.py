from pico2d import *

import game_framework
import world

PIXEL_PER_METER = 60.0
RUN_SPEED_KMPH = 12.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class Run:
    def __init__(self,player):
        self.player = player
        self.image_right = load_image('_Run.png')
        self.image_left = load_image('_Run_R.png')
        self.image = self.image_right
        self.frame = 0

    def enter(self,event):
        frame_time = game_framework.frame_time
        self.frame = (self.frame + 1) % 10
        self.player.x += RUN_SPEED_PPS * frame_time * self.player.dir

        if right_down(event) or left_up(event):
            self.player.dir = 1
        elif left_down(event) or right_up(event):
            self.player.dir = -1

        # if self.player.dir == 1:
        #     self.image = self.image_right
        # elif self.player.dir == -1:
        #     self.image = self.image_left

    def exit(self,event):
        pass

    def do(self):
        self.frame = (self.frame + 1) % 10
        self.player.x += 15 * self.player.dir

        if self.player.x > world.right_boundary:
            self.player.x = world.right_boundary
        if self.player.x < world.left_boundary:
            self.player.x = world.left_boundary

    def draw(self):
        if self.player.dir == 1:
            self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h,self.player.x, self.player.y, self.player.w * 3, self.player.h * 3)
        else :
            self.image.clip_composite_draw(self.frame * self.player.w, 0, self.player.w, self.player.h,0, 'h',self.player.x, self.player.y, self.player.w * 3, self.player.h * 3)