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

class DungeonMap:
    def __init__(self):
        self.tiles = []
        self.make_tiles()

    def make_tiles(self):
        for i in range(0,21):
            self.tiles.append(DungeonTile(32+i*32,80,0,8))

        for i in range(5, 10):
            self.tiles.append(DungeonTile(32 + i * 32, 200, 1, 8))

        for i in range(12, 16):
            self.tiles.append(DungeonTile(32 + i * 32, 320, 2, 8))

    def draw(self):
        for t in self.tiles:
            t.draw()

    def get_tiles(self):
        return self.tiles