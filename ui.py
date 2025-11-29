from pico2d import *

class GameUI:
    def __init__(self):
        self.sheet = load_image('UI.png')

        self.HEART_W = 16
        self.HEART_H = 16

        self.full_x, self.full_y = 136, 136
        self.half_x, self.half_y = 168, 136
        self.empty_x, self.empty_y = 200, 136

    def draw_hp(self, hp, max_hp=6):
        hearts = max_hp // 2
        start_x = 40
        y = 680

        full = hp // 2
        half = hp % 2

        index = 0

        for _ in range(full):
            x = start_x + index * 40
            self.sheet.clip_draw(self.full_x, self.full_y,self.HEART_W, self.HEART_H,x, y, 32, 32)
            index += 1

        if half == 1:
            x = start_x + index * 40
            self.sheet.clip_draw(self.half_x, self.half_y,self.HEART_W, self.HEART_H,x, y, 32, 32)
            index += 1

        while index < hearts:
            x = start_x + index * 40
            self.sheet.clip_draw(self.empty_x, self.empty_y,self.HEART_W, self.HEART_H, x, y, 32, 32)
            index += 1
