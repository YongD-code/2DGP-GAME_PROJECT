from pico2d import *
import world
from idle import Idle
from state_machine import StateMachine
from run import Run
from harvest import Harvest
from crop import Crop

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
def c_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def c_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c
def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x
def x_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_x


class Player:
    def __init__(self):
        self.image = load_image('_idle.png')
        self.x,self.y = 80,228
        self.frame = 0
        self.w = 120
        self.h = 80
        self.dir = 1
        self.right_input = False
        self.left_input = False
        self.lock_dir = 1

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.HARVEST = Harvest(self)
        self.ROLL = Roll(self)
        self.ATTACK = Attack(self)
        self.JUMP = Jump(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.RUN,left_down:self.RUN, down_down:self.HARVEST, z_down:self.ROLL,c_down: self.ATTACK,x_down: self.JUMP},
                self.RUN: {right_up: self.IDLE,left_up:self.IDLE,z_down:self.ROLL,c_down: self.ATTACK,x_down: self.JUMP},
                self.HARVEST:{down_up: self.IDLE},
                self.ROLL:{right_down:self.RUN,left_down:self.RUN},
                self.ATTACK:{right_down:self.RUN,left_down:self.RUN},
                self.JUMP:{}
            },
            self
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.right_input = True
                self.dir = 1
            elif event.key == SDLK_LEFT:
                self.left_input = True
                self.dir = -1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.right_input = False
            elif event.key == SDLK_LEFT:
                self.left_input = False

        if self.state_machine.current_state == self.ROLL:
            return
        self.state_machine.handle_state_event(('INPUT',event))

    def find_crop(self):
        global crops
        for crop in world.crops:
            if (self.x - 32 < crop.x < self.x + 32) and (self.y - 16 < crop.y < self.y + 32):
                return crop
        return None

class Roll:
    def __init__(self,player):
        self.player = player
        self.image_right = load_image('roll.png')
        self.image_left = load_image('roll_R.png')
        self.image = self.image_right
        self.frame = 0
        self.prev_state = None

    def enter(self,event):
        self.player.lock_dir = self.player.dir

        if self.player.dir == 1:
            self.frame = 0
            self.image = self.image_right

        elif self.player.dir == -1:
            self.frame = 11
            self.image = self.image_left

    def exit(self,event):
        pass

    def do(self):
        if self.player.lock_dir == 1:
            self.frame += 1
            check_RL =  self.frame>=12

        else:
            self.frame -= 1
            check_RL = self.frame<0

        self.player.x += 15 * self.player.lock_dir

        if check_RL:
            if self.player.right_input:
                self.player.dir = 1
                self.player.state_machine.change_state(self.player.RUN)
            elif self.player.left_input:
                self.player.dir = -1
                self.player.state_machine.change_state(self.player.RUN)
            else:
                self.player.state_machine.change_state(self.player.IDLE)

        if self.player.x > 1250:
            self.player.x = 1250
        if self.player.x < 30:
            self.player.x = 30

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 3,self.player.h * 3)

class Jump:
    def __init__(self,player):
        self.player = player
        self.image_jump_right = load_image('jump.png')
        self.image_jump_left = load_image('jump_R.png')

        self.image_fall_right = load_image('jump_fall.png')
        self.image_fall_left = load_image('jump_fall_R.png')

        self.image = self.image_jump_right
        self.frame = 0
        self.prev_state = None

    def enter(self,event):
        self.frame = 0

        if self.player.dir == 1:
            self.image = self.image_jump_right
        elif self.player.dir == -1:
            self.image = self.image_jump_left

        self.player.jump_y = 18
        if self.prev_state == self.player.RUN:
            self.player.jump_x = 10 * self.player.dir
        else:
            self.player.jump_x = 0

    def exit(self,event):
        self.player.jump_x = 0
        self.player.jump_y = 0
        pass

    def do(self):
        self.player.jump_y -= 2.5
        self.player.y += self.player.jump_y
        self.player.x += self.player.jump_x

        self.frame += 1.5

        if self.player.jump_y > 2:
            self.image = self.image_jump_right if self.player.dir == 1 else self.image_jump_left
            if self.frame >= 3:
                self.frame = 2.9
        else:
            self.image = self.image_fall_right if self.player.dir == 1 else self.image_fall_left
            if self.frame >= 2:
                self.frame = 1.9

        if self.player.y <= 228:
            self.player.y = 228
            if self.player.right_input or self.player.left_input:
                self.player.state_machine.change_state(self.player.RUN)
            else:
                self.player.state_machine.change_state(self.player.IDLE)

        if self.player.x > 1250:
            self.player.x = 1250
        if self.player.x < 30:
            self.player.x = 30

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 3,self.player.h * 3)

class Attack:
    def __init__(self,player):
        self.player = player
        self.image_right = load_image('attack.png')
        self.image_left = load_image('attack_R.png')
        self.image = self.image_right
        self.frame = 0

    def enter(self,event):
        self.player.lock_dir = self.player.dir

        if self.player.dir == 1:
            self.frame = 0
            self.image = self.image_right

        elif self.player.dir == -1:
            self.frame = 9
            self.image = self.image_left

    def exit(self,event):
        pass

    def do(self):
        if self.player.lock_dir == 1:
            self.frame += 1
            check_RL =  self.frame>=10

        else:
            self.frame -= 1
            check_RL = self.frame<0

        if check_RL:
            if self.player.right_input:
                self.player.dir = 1
                self.player.state_machine.change_state(self.player.RUN)
            elif self.player.left_input:
                self.player.dir = -1
                self.player.state_machine.change_state(self.player.RUN)
            else:
                self.player.state_machine.change_state(self.player.IDLE)

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 2.9,self.player.h * 2.9)