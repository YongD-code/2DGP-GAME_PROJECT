from pico2d import *

from idle import Idle
from state_machine import StateMachine
from run import Run
from harvest import Harvest

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN
def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z
def z_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_z

class Player:
    def __init__(self):
        self.image = load_image('_idle.png')
        self.x,self.y = 80,228
        self.frame = 0
        self.w = 120
        self.h = 80
        self.dir = 1

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.HARVEST = Harvest(self)
        self.ROLL = Roll(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.RUN,left_down:self.RUN, down_down:self.HARVEST, z_down:self.ROLL},
                self.RUN: {right_up: self.IDLE,left_up:self.IDLE,z_down:self.ROLL},
                self.HARVEST:{down_up: self.IDLE},
                self.ROLL:{}
            },
            self
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))



class Roll:
    def __init__(self,player):
        self.player = player
        self.image_right = load_image('roll.png')
        self.image_left = load_image('roll_R.png')
        self.image = self.image_right
        self.frame = 0
        self.prev_state = None

    def enter(self,event):
        self.frame = 0
        if self.player.dir == 1:
            self.frame = 0
            self.image = self.image_right
        elif self.player.dir == -1:
            self.frame = 11
            self.image = self.image_left

    def exit(self,event):
        pass

    def do(self):
        if self.player.dir == 1:
            self.frame += 1
            check_RL =  self.frame>=12

        else:
            self.frame -= 1
            check_RL = self.frame<0

        self.player.x += 15 * self.player.dir

        if check_RL:
            if self.prev_state == self.player.RUN:
                self.player.state_machine.change_state(self.player.RUN)
            else:
                self.player.state_machine.change_state(self.player.IDLE)

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 3,self.player.h * 3)

class Jump:
    def __init__(self,player):
        self.player = player
        self.image_right = load_image('jump.png')
        self.image_left = load_image('jump_R.png')
        self.image = self.image_right
        self.frame = 0

    def enter(self,event):
        self.frame = 0

        if self.player.dir == 1:
            self.image = self.image_right
        elif self.player.dir == -1:
            self.image = self.image_left

    def exit(self,event):
        pass

    def do(self):
        if self.frame < 5:
            self.frame += 1
        else:
            self.frame = 5

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 3,self.player.h * 3)

class Attack:
    def __init__(self,player):
        self.player = player
        self.image_right = load_image('attack.png')
        self.image_left = load_image('attack_R.png')
        self.image = self.image_right
        self.frame = 0

    def enter(self,event):
        self.frame = 0

        if self.player.dir == 1:
            self.image = self.image_right
        elif self.player.dir == -1:
            self.image = self.image_left

    def exit(self,event):
        pass

    def do(self):
        if self.frame < 5:
            self.frame += 1
        else:
            self.frame = 5

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 3,self.player.h * 3)