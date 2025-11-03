from pico2d import *
import world

class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(640, 360)

class Blacksmith:
    def __init__(self):
        self.image = load_image('Blacksmith.png')
        self.frame = 1
        self.w ,self.h = 288,170
        self.x, self.y = 290,190
        self.last_time = get_time()
        self.frame_interval = 0.1

    def update(self):
        current_time = get_time()
        if current_time - self.last_time > self.frame_interval:
            self.frame += 1
            if self.frame > 4:
                self.frame = 1
            self.last_time = current_time

    def draw(self):
        self.image.clip_draw(self.frame * self.w, 0, self.w , self.h, self.x, self.y,self.w*1.2 , self.h*1.2)


class Ground:
    def __init__(self):
        self.image = load_image('Tile_ground.png')
        self.farm_image = load_image('Farm_Tile.png')
        self.tile_w = 32
        self.tile_h = 32
        self.tile_count = 1280//self.tile_w
        self.farmable_tiles = list(range(15, 25))

    def can_plant(self,tile_x,tile_y):
        return tile_y == 3 and tile_x in self.farmable_tiles

    def update(self):
        pass

    def draw_tile(self, row, col, x, y):
        left = col * self.tile_w
        bottom = self.image.h - (row + 1) * self.tile_h
        self.image.clip_draw(left, bottom, self.tile_w, self.tile_h, x, y)

    def draw(self):
        for i in range(self.tile_count):
            x = i * self.tile_w + self.tile_w // 2
            if 15 <= i <= 24:
                y = self.tile_h * 0
                self.draw_tile(2, 1, x, y)
                y = self.tile_h * 1
                self.draw_tile(1, 1, x, y)
                y = self.tile_h * 2
                self.draw_tile(1, 1, x, y)
                y = self.tile_h * 3
                self.farm_image.clip_draw(128,96,32,32,x,y)
            else:
                y = self.tile_h * 0
                self.draw_tile(2, 1, x, y)
                y = self.tile_h * 1
                self.draw_tile(1, 1, x, y)
                y = self.tile_h * 2
                self.draw_tile(1, 1, x, y)
                y = self.tile_h * 3
                self.draw_tile(0, 1, x, y)


class Portal:
    def __init__(self):
        self.image = load_image('portal.png')
        self.w,self.h = 64,64
        self.frame = 0
        self.frame_row = [4,3]
        self.frame_count = 0
        self.x,self.y = 70, 180
        self.timer = 0
        self.timer_delay = 0.6
        self.radius = 80

    def update(self):
        self.timer += 0.3
        if self.timer > self.timer_delay:
            self.frame = (self.frame+1) % 7
            self.timer = 0
        pass

    def draw(self):
        if self.frame < 4:
            row = 1
            col = self.frame
        else:
            row = 0
            col = self.frame - 4

        left = col * self.w
        bottom = row * self.h

        self.image.clip_draw(left, bottom, self.w, self.h, self.x, self.y,self.w*3,self.h*3)
        pass

class House:
    def __init__(self):
        self.image = load_image('player_house.png')
        self.x, self.y = 1024, 288
        self.w, self.h = 512,512

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0,0,self.w,self.h,self.x, self.y,self.w * 0.8,self.h * 1)

