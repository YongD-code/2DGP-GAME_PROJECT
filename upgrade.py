from pico2d import *
import world
from text_ani import TextAni

class Upgrade:
    def __init__(self):
        self.bg = load_image('dialogue_box.png')
        self.font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 26)
        self.active = True

    def draw(self):
        self.bg.draw(640, 120, 600, 120)
        player = world.player
        next_cost = (player.damage_level + 1) * 50
        next_power = player.damage + 10

        self.font.draw(400, 140,
            f"공격력 강화", (0,0,0))
        self.font.draw(400, 110,
            f"Gold {next_cost} 사용 → 공격력 {player.damage} → {next_power}", (0,0,0))
        self.font.draw(400, 80,
            "강화하려면 SPACE를 누르세요!", (0,0,0))

    def upgrade(self):
        player = world.player
        cost = (player.damage_level + 1) * 50

        if world.gold < cost:
            world.add_object(TextAni(player.x, player.y + 60, "골드가 부족합니다!", (255,120,120)), 3)
            self.active = False
            return

        world.gold -= cost
        player.damage += 1
        player.damage_level += 1

        world.add_object(TextAni(player.x, player.y + 60, "공격력 +10!", (255,255,100)), 3)

        self.active = False
