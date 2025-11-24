from pico2d import *
import world

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

    def text_dead(self):
        return self.alpha <= 0

    def draw(self):
        r, g, b = int(self.color[0] * self.alpha), int(self.color[1] * self.alpha), int(self.color[2] * self.alpha)
        self.font.draw(self.x, self.y, self.text, (r, g, b))

class DeathTextAni:
    def __init__(self):
        self.x = 440   # 중앙 정렬 보정 (YOU DIED 라서 조금 왼쪽)
        self.y = 360
        self.text = "YOU DIED"
        self.alpha = 1.0
        self.timer = 0
        self.duration = 1.8
        self.font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 90)  # 큰 글씨!
        self.color = (255, 0, 0)  # 붉게

    def update(self, frame_time):
        self.timer += frame_time

        # 위로 천천히 상승
        self.y += 40 * frame_time

        # 후반부에 알파 감소
        if self.timer > self.duration * 0.4:
            self.alpha -= (frame_time / (self.duration * 0.6))
            if self.alpha < 0:
                self.alpha = 0

        # 애니메이션 끝 → 타이틀로 자동 이동
        if self.timer >= self.duration:
            import game_framework
            import title_mode
            game_framework.change_mode(title_mode)

    def draw(self):
        r = int(self.color[0] * self.alpha)
        g = int(self.color[1] * self.alpha)
        b = int(self.color[2] * self.alpha)

        self.font.draw(self.x, self.y, self.text, (r, g, b))

class DamageTextAni:
    def __init__(self, x, y, damage, color=(255, 80, 80)):
        self.x = x
        self.y = y
        self.text = str(damage)
        self.alpha = 1.0
        self.timer = 0
        self.duration = 0.9
        self.font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 28)
        self.color = color

    def update(self, frame_time):
        self.timer += frame_time
        self.y += 60 * frame_time  # 더 빠르게 위로

        if self.timer > self.duration * 0.4:
            self.alpha -= (frame_time / (self.duration * 0.6))
            if self.alpha < 0:
                self.alpha = 0

    def text_dead(self):
        return self.alpha <= 0

    def draw(self):
        r = int(self.color[0] * self.alpha)
        g = int(self.color[1] * self.alpha)
        b = int(self.color[2] * self.alpha)

        self.font.draw(self.x - 10, self.y, self.text, (r, g, b))

