from pico2d import *


class Run:
    def __init__(self,player):
        self.player = player
    def enter(self,event):
        self.image = load_image('_Run.png')
        self.frame = 0

    def exit(self,event):
        pass

    def do(self):
        self.frame = (self.frame + 1) % 10
        self.player.x += 5 * self.player.dir
        if self.player.x > 1160:
            self.player.dir = 0
        if self.player.x < 120:
            self.player.dir = 0

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h,self.player.x, self.player.y, self.player.w * 3, self.player.h * 3)
