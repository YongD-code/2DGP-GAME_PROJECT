from pico2d import *

class TextAni:
    def __init__(self, x, y, text, color=(255,255,255),duration=1.5):
        self.x = x
        self.y = y
        self.text = text
        self.alpha = 1.0
        self.timer = 0
        self.duration = duration
        self.font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 20)
        self.color = color

    def update(self, frame_time):
        self.timer += frame_time
        self.y += 30 * frame_time
        if self.timer > self.duration * 0.5:
            self.alpha -= (frame_time / (self.duration * 0.5))
            if self.alpha < 0:
                self.alpha = 0

        if self.alpha < 0:
            self.alpha = 0

    def is_dead(self):
        return self.alpha <= 0

    def draw(self):
        r, g, b = int(self.color[0] * self.alpha), int(self.color[1] * self.alpha), int(self.color[2] * self.alpha)
        self.font.draw(self.x, self.y, self.text, (r, g, b))
