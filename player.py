from pico2d import load_image

from idle import Idle
from state_machine import StateMachine
from run import Run

class Player:
    def __init__(self):
        self.image = load_image('_idle.png')
        self.x,self.y = 80,120
        self.frame = 0
        self.w = 120
        self.h = 80
        self.dir = 1
        self.state_machine = StateMachine(Idle, self)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def change_state(self, new_state):
        self.state_machine.change_state(new_state)