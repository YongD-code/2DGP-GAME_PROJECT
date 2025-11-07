from pico2d import *
import world
from idle import Idle
from state_machine import StateMachine
from run import Run
from harvest import Harvest,Plant
import game_framework


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
def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


PIXEL_PER_METER = 60.0

RUN_SPEED_KMPH = 12.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

ROLL_SPEED_KMPH = 20.0
ROLL_SPEED_MPS = (ROLL_SPEED_KMPH * 1000.0 / 3600.0)
ROLL_SPEED_PPS = ROLL_SPEED_MPS * PIXEL_PER_METER

JUMP_SPEED_MPS = 8.0
JUMP_SPEED_PPS = JUMP_SPEED_MPS * PIXEL_PER_METER

GRAVITY_MPS = 14
GRAVITY_PPS = GRAVITY_MPS * PIXEL_PER_METER

FPS_ROLL = 0.9
FPS_JUMP = 8.0
FPS_ATTACK = 20.0

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
        self.vx = 0.0
        self.vy = 0.0
        self.attack_queued = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.HARVEST = Harvest(self)
        self.ROLL = Roll(self)
        self.ATTACK = Attack(self)
        self.JUMP = Jump(self)
        self.PLANT = Plant(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.RUN,left_down:self.RUN, down_down:self.HARVEST, z_down:self.ROLL,c_down: self.ATTACK,x_down: self.JUMP,s_down:self.PLANT},
                self.RUN: {right_up: self.IDLE,left_up:self.IDLE,z_down:self.ROLL,c_down: self.ATTACK,x_down: self.JUMP},
                self.HARVEST:{down_up: self.IDLE},
                self.ROLL:{right_down:self.RUN,left_down:self.RUN},
                self.ATTACK:{right_down:self.RUN,left_down:self.RUN},
                self.JUMP:{},
                self.PLANT: {s_up: self.IDLE}
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
            elif event.key == SDLK_UP:
                if self.on_portal():
                    import dungeon_mode
                    game_framework.change_mode(dungeon_mode)
            elif event.key == SDLK_x:
                if self.state_machine.current_state in [self.ROLL, self.ATTACK, self.HARVEST, self.PLANT]:
                    return
                if self.state_machine.current_state == self.JUMP:
                    if self.JUMP.jump_count < self.JUMP.max_jump:
                        self.JUMP.enter(event)
                else:
                    self.state_machine.change_state(self.JUMP)

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

    def on_portal(self):
        portal = world.portal
        if portal is None:
            return False

        dx = self.x - portal.x
        dy = self.y - portal.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance < portal.radius

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
        frame_time = FPS_ROLL * game_framework.frame_time
        if self.player.lock_dir == 1:
            self.frame += 1
            check_RL =  self.frame>=12

        else:
            self.frame -= 1
            check_RL = self.frame<0

        self.player.x += ROLL_SPEED_PPS * frame_time * self.player.lock_dir

        if check_RL:
            if self.player.right_input:
                self.player.dir = 1
                self.player.state_machine.change_state(self.player.RUN)
            elif self.player.left_input:
                self.player.dir = -1
                self.player.state_machine.change_state(self.player.RUN)
            else:
                self.player.state_machine.change_state(self.player.IDLE)

        if self.player.x > world.right_boundary:
            self.player.x = world.right_boundary
        if self.player.x < world.left_boundary:
            self.player.x = world.left_boundary

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

        self.jump_count = 0
        self.max_jump = 2

    def enter(self,event):
        self.frame = 0

        if self.player.dir == 1:
            self.image = self.image_jump_right
        elif self.player.dir == -1:
            self.image = self.image_jump_left

        if self.jump_count == 0:
            self.player.vy = JUMP_SPEED_PPS
        else:
            self.player.vy = JUMP_SPEED_PPS * 0.9

        if self.player.right_input:
            self.player.vx = RUN_SPEED_PPS
            self.player.dir = 1
        elif self.player.left_input:
            self.player.vx = -RUN_SPEED_PPS
            self.player.dir = -1
        else:
            self.player.vx = 0

        self.player.on_ground = False
        self.jump_count += 1

    def exit(self,event):
        self.player.jump_x = 0
        self.player.jump_y = 0

    def do(self):
        frame_time = game_framework.frame_time

        self.player.vy -= GRAVITY_PPS * frame_time
        self.player.y += self.player.vy * frame_time
        self.player.x += self.player.vx * frame_time

        self.frame += FPS_JUMP * frame_time
        if self.player.vy > 0:  # 상승
            if self.frame >= 3:
                self.frame = 2.9
            self.image = self.image_jump_right if self.player.dir == 1 else self.image_jump_left
        else:  # 하강
            if self.frame >= 2:
                self.frame = 1.9
            self.image = self.image_fall_right if self.player.dir == 1 else self.image_fall_left

        if self.player.y <= world.ground_y:
            self.player.y = world.ground_y
            self.player.vy = 0
            self.jump_count = 0
            self.player.on_ground = True
            if self.player.right_input or self.player.left_input:
                self.player.state_machine.change_state(self.player.RUN)
            else:
                self.player.state_machine.change_state(self.player.IDLE)

        if self.player.x > world.right_boundary:
            self.player.x = world.right_boundary
        if self.player.x < world.left_boundary:
            self.player.x = world.left_boundary

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 3,self.player.h * 3)

class Attack:
    def __init__(self,player):
        self.player = player
        self.image_right = load_image('attack.png')
        self.image_left = load_image('attack_R.png')
        self.image = self.image_right
        self.frame = 0
        self.combo = 1
        self.combo_timer = 0.0
        self.combo_delay = 0.5
        self.combo_input = False
        self.waiting_combo = False
        self.done = False

    def enter(self,event):
        self.player.lock_dir = self.player.dir
        self.combo = 1
        self.combo_timer = 0.0
        self.waiting_combo = False
        self.done = False

        if self.player.dir == 1:
            self.frame = 0
            self.image = self.image_right

        elif self.player.dir == -1:
            self.frame = 9
            self.image = self.image_left
        self.combo = 1
    def handle_event(self, event):
        if event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_c:
            if self.combo == 1 and self.combo_timer > 0.0:
                self.combo_input = True

    def exit(self,event):
        pass

    def do(self):
        frame_time = game_framework.frame_time
        fps = FPS_ATTACK * frame_time

        if self.player.lock_dir == 1:
            self.frame += fps
            if self.frame >= 9.9:
                if self.player.right_input:
                    self.player.state_machine.change_state(self.player.RUN)
                elif self.player.left_input:
                    self.player.state_machine.change_state(self.player.RUN)
                else:
                    self.player.state_machine.change_state(self.player.IDLE)

        else:
            self.frame -= fps
            if self.frame <= 0.1:
                if self.player.right_input:
                    self.player.state_machine.change_state(self.player.RUN)
                elif self.player.left_input:
                    self.player.state_machine.change_state(self.player.RUN)
                else:
                    self.player.state_machine.change_state(self.player.IDLE)

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 2.9,self.player.h * 2.9)