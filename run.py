from pico2d import *

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
        self.frame = 0

        if right_down(event) or left_up(event):
            self.player.dir = 1
        elif left_down(event) or right_up(event):
            self.player.dir = -1

        if self.player.dir == 1:
            self.image = self.image_right
        elif self.player.dir == -1:
            self.image = self.image_left

    def exit(self,event):
        pass

    def do(self):
        self.frame = (self.frame + 1) % 10
        self.player.x += 15 * self.player.dir

        if self.player.x > 1240:
            self.player.dir = 0
        if self.player.x < 40:
            self.player.dir = 0

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h,self.player.x, self.player.y, self.player.w * 3, self.player.h * 3)
