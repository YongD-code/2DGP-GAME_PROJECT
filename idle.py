from pico2d import *

class Idle:
    def enter(self,event):
        self.image = load_image('_Idle.png')
        self.frame = 0

    def exit(self,event):
        pass

    def do(self):
        self.frame = (self.frame + 1) % 10

    def draw(self):
        self.image.clip_draw(self.frame * self.w, 0, self.w, self.h, self.x, self.y, self.w * 3,self.h * 3)