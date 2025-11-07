from pico2d import *

class DungeonTile:
    def __init__(self, x, y,col = 0, row = 0):
        self.x = x
        self.y = y
        self.image = load_image('Dungeon_Tile.png')
        self.w, self.h = 16, 16
        self.col = col
        self.row = row

    def draw(self):
        left = self.col * self.w
        bottom = self.image.h - (self.row + 1) * self.h
        self.image.clip_draw(left, bottom, self.w, self.h, self.x, self.y,self.w*2,self.h*2)
