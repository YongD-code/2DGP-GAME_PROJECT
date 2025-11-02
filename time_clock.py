from pico2d import *

class GameTime:
    def __init__(self):
        self.image = load_image('clock_UI.png')
        self.x, self.y = 1150, 662
        self.w, self.h = 96,32
        self.font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 30)
        self.total_time = 0.0
        self.hour = 6
        self.minute = 0.0
        self.time_speed = 5.0

    def update(self,frame_time):
        self.total_time += frame_time * self.time_speed
        self.minute += frame_time * self.time_speed

        if self.minute > 60:
            self.minute -= 60
            self.hour += 1

        if self.hour >= 24:
            self.hour = 0

    def draw(self):
        self.image.clip_draw(0,0, self.w, self.h,self.x, self.y,self.w*2,self.h*2)
        display_minute = int(self.minute // 10 * 10)
        time_text = f"{int(self.hour):02d}:{int(display_minute):02d}"
        self.font.draw(1110, 660, f"{time_text}", (0, 0, 0))
