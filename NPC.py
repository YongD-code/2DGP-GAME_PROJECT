from pico2d import *
import world
import game_framework

class Npc:
    def __init__(self):
        self.right_frames = [load_image(f'NPC_Idle{i}.png') for i in range(1,10)]
        self.left_frames = [load_image(f'NPC_Idle{i}_R.png') for i in range(1,10)]
        self.frame_index = 0
        self.x, self.y = 1060, 180
        self.w,self.h = 64,64
        self.timer = 0
        self.timer_delay = 0.15
        self.face = True

        self.dialogue_intro = [
            "혹시 나를 좀 도와줄 수 있을까?"
        ]

        self.dialogue_quest = [
            "옥수수 5개만 구해다 줄래?",
        ]

        self.dialogue_complete = [
            "증말 고마워~!! 이건 보상이야."
        ]

    def update(self,player_x = None):
        frame_time = game_framework.frame_time
        if world.player.x > self.x:
            self.face = True
        else:
            self.face = False

        self.timer += frame_time
        if self.timer > self.timer_delay:
            self.frame_index = (self.frame_index + 1) % 9
            self.timer = 0

    def draw(self):
        if self.face:
            self.right_frames[self.frame_index].draw(self.x, self.y, self.w*2.5,self.h*2.5)
        else:
            self.left_frames[self.frame_index].draw(self.x, self.y, self.w*2.5,self.h*2.5)

    def can_talk(self):
        px = world.player.x
        return abs(self.x - px) < 80

