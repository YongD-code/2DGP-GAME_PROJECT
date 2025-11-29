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
        self.face = True
        self.fps = 10.0
        self.total_frames = 9

        self.quest_ids = ["quest_corn", "quest_slime"]

        self.dialogue_intro = {
            "quest_corn": ["안녕 농부야 내가 뭐 좀 부탁해도 될까?!"],
            "quest_slime": ["이번엔 몬스터 처리 좀 부탁해도 될까?"],
        }

        self.dialogue_quest = {
            "quest_corn": ["옥수수 5개 모아줘"],
            "quest_slime": ["슬라임 10마리만 잡아줘"],
        }

        self.dialogue_in_progress = {
            "quest_corn": ["옥수수를 좀 더 열심히 키워야겠는데?"],
            "quest_slime": ["슬라임 잡기가 아직은 좀 무서운가봐?"],
        }

        self.dialogue_complete = {
            "quest_corn": ["옥수수 정도는 별 거 아닌가 보네?","다음 일도 맡겨도 되지?"],
            "quest_slime": ["귀여운 슬라임들을 벌써 다 잡은거야? 고마워!"],
        }

    def update(self,player_x = None):
        frame_time = game_framework.frame_time
        if world.player.x > self.x:
            self.face = True
        else:
            self.face = False

        self.frame_index += self.fps * frame_time
        if self.frame_index >= self.total_frames:
            self.frame_index -= self.total_frames

    def draw(self):
        frame = int(self.frame_index)
        if self.face:
            img = self.right_frames[frame]
        else:
            img = self.left_frames[frame]

        img.draw(self.x, self.y, self.w * 2.5, self.h * 2.5)

    def can_talk(self):
        px = world.player.x
        return abs(self.x - px) < 80

