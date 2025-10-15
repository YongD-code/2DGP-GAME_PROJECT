from pico2d import load_image

from idle import Idle


class Player:
    def __init__(self):
        self.image = load_image('_idle.png')
        self.x,self.y = 80,120
        self.frame = 0
        self.w = 120
        self.h = 80
        self.state = Idle

    def update(self):
        self.state.update(self)

    def draw(self):
        self.state.draw(self)
