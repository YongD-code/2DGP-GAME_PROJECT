from pico2d import *

SCALE = 2.5

class DungeonTile:
    def __init__(self, x, y,col = 0, row = 0):
        self.x = x
        self.y = y
        self.image = load_image('Dungeon_Tile.png')
        self.w, self.h = 16, 16
        self.col = col
        self.row = row

    def update(self):
        pass

    def draw(self):
        left = self.col * self.w
        bottom = self.image.h - (self.row + 1) * self.h
        self.image.clip_draw(left, bottom, self.w, self.h, self.x, self.y,self.w * SCALE,self.h * SCALE)
        #바운딩 박스 확인용 나중에 삭제할 예정
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        half_w = (self.w * SCALE) / 2
        half_h = (self.h * SCALE) / 2
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

class DungeonMap:
    def __init__(self,stage_num = 1):
        self.stage_num = stage_num
        self.tiles = []
        if stage_num == 1:
            self.make_tiles_1()
        elif stage_num == 2:
            self.make_tiles_2()
        elif stage_num == 3:
            self.make_tiles_3()

    def make_tiles_1(self):
        for i in range(0,21):
            self.tiles.append(DungeonTile(86+i*32,240,1,2))

        for i in range(29, 38):
            self.tiles.append(DungeonTile(16 + i * 32, 340, 1, 2))

        for i in range(0, 16):
            self.tiles.append(DungeonTile(86 + i * 32, 470, 1, 2))

    def make_tiles_2(self):
        for i in range(0,21):
            self.tiles.append(DungeonTile(86+i*32,240,1,2))

        for i in range(18, 38):
            self.tiles.append(DungeonTile(16 + i * 32, 440, 1, 2))
        pass

    def make_tiles_3(self):
        pass

    def get_tile(self):
        return self.tiles

    def update(self):
        pass

    def draw(self):
        for t in self.tiles:
            t.draw()

    def get_tiles(self):
        return self.tiles

    def handle_collision(self, group, other):
        pass