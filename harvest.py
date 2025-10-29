from pico2d import *
from crop import Crop

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

class Harvest:
    def __init__(self,player):
        self.player = player
        self.image_right = load_image('harvest.png')
        self.image_left = load_image('harvest_R.png')
        self.image = self.image_right
        self.frame = 0
        self.action = None
        self.check_crop = None

    def enter(self,event):
        self.frame = 0
        if self.player.dir == 1:
            self.image = self.image_right
        elif self.player.dir == -1:
            self.image = self.image_left

        self.check_crop = self.player.find_crop()

        if self.check_crop:
            self.action = 'harvest'
        else:
            self.action = 'plant'

    def exit(self,event):
        self.action = None
        self.check_crop = None
        pass

    def do(self):
        global crops

        self.frame += 1
        if self.frame >= 3:
            if self.action == 'harvest' and self.check_crop:
                self.check_crop.harvest()
            elif self.action == 'plant':
                crops.append(Crop(self.player.x, 96))
            self.player.state_machine.change_state(self.player.IDLE)

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 3,self.player.h * 3)