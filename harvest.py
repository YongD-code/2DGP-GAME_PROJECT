from pico2d import *
from crop import Crop
import world

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

    def enter(self,event):
        self.frame = 0
        if self.player.dir == 1:
            self.image = self.image_right
        elif self.player.dir == -1:
            self.image = self.image_left

        check_crop = self.player.find_crop()
        if check_crop:
            world.crops.remove(check_crop)
        else:
            world.crops.append(Crop(self.player.x, 120))

    def exit(self,event):
        pass

    def do(self):
        if self.frame < 2:
            self.frame += 1
        else:
            self.frame = 2

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 3,self.player.h * 3)