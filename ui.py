from pico2d import *

class GameUI:
    def __init__(self):
        self.sheet = load_image('UI.png')
        self.gold_sheet = load_image('gold.png')
        self.font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 10)
        self.HEART_W = 16
        self.HEART_H = 16

        self.full_x, self.full_y = 136, 136
        self.half_x, self.half_y = 168, 136
        self.empty_x, self.empty_y = 200, 136

        self.gold_frame = 0.0
        self.gold_total_frames = 6
        self.gold_w = 80
        self.gold_h = 80
        self.fps = 12.0

    def update(self, frame_time):
        self.gold_frame += self.fps * frame_time

        if self.gold_frame >= self.gold_total_frames:
            self.gold_frame -= self.gold_total_frames

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

    def draw_gold(self, gold_amount):
        x = 40
        y = 640
        current_frame = int(self.gold_frame)

        self.gold_sheet.clip_draw(current_frame * self.gold_w, 0 ,self.gold_w, self.gold_h,x, y, 32, 32)

        self.font.draw(x + 40, y - 10, f"{gold_amount}", (255,255,255))