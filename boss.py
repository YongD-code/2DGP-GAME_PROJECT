from pico2d import *
import math
import world
from text_ani import DamageTextAni
from behavior_tree import BehaviorTree, Action, Condition, Sequence, Selector
import game_framework

BOSS_W = 288
BOSS_H = 160

BOSS_BB_W = 120
BOSS_BB_H = 250


class Boss:
    image = None
    hp_bar = load_image('hp.png')
    boss_hit_sound = None
    boss_attack_sound = None
    boss_dead_sound = None
    boss_rage_sound = None

    IDLE_ROW = 4
    WALK_ROW = 3
    ATTACK_ROW = 2
    HIT_ROW = 1
    DEAD_ROW = 0

    IDLE_FRAME_COUNT = 6
    WALK_FRAME_COUNT = 12
    ATTACK_FRAME_COUNT = 15
    HIT_FRAME_COUNT = 5
    DIE_FRAME_COUNT = 22

    IDLE = 0
    ATTACK = 1
    DEAD = 2
    WALK = 3
    HIT = 4

    ATTACK_RANGE = 250
    ATTACK_COOL = 2.0

    def __init__(self, x, y):
        if Boss.image is None:
            Boss.image = load_image('Boss.png')

        if not Boss.boss_hit_sound:
            Boss.boss_hit_sound = load_wav('sound/boss_hit.wav')
            Boss.boss_hit_sound.set_volume(32)

        if not Boss.boss_attack_sound:
            Boss.boss_attack_sound = load_wav('sound/boss_attack.wav')
            Boss.boss_attack_sound.set_volume(32)

        if not Boss.boss_dead_sound:
            Boss.boss_dead_sound = load_wav('sound/boss_dead.wav')
            Boss.boss_dead_sound.set_volume(64)

        if not Boss.boss_rage_sound:
            Boss.boss_rage_sound = load_wav('sound/rage.wav')
            Boss.boss_rage_sound.set_volume(32)

        self.x, self.y = x, y
        self.hp = 300
        self.max_hp = self.hp
        self.damage = 3
        self.state = Boss.IDLE
        self.dir = 1

        self.frame = 0.0
        self.frame_per_sec = 8.0
        self.speed = 50.0

        self.attack_processed = False
        self.attack_cool = 0.0

        self.hit_timer = 0.0
        self.is_dead = False

        self.w, self.h = BOSS_W, BOSS_H
        self.ground_y = world.ground_y
        self.rage = False

        self.build_behavior_tree()

    def distance_to_player(self):
        px = world.player.x
        return abs(px - self.x)


    def player_is_near(self, r):
        return self.distance_to_player() < r


    def player_near(self, r):
        return BehaviorTree.SUCCESS if self.player_is_near(r) else BehaviorTree.FAIL


    def attack_ready(self):
        return BehaviorTree.SUCCESS if self.attack_cool <= 0 else BehaviorTree.FAIL


    def action_attack(self):
        self.state = Boss.ATTACK
        self.frame = 0.0
        self.attack_processed = False
        if self.hp < self.max_hp / 2:
            self.attack_cool = Boss.ATTACK_COOL / 2
        else:
            self.attack_cool = Boss.ATTACK_COOL
        return BehaviorTree.SUCCESS

    def action_chase_player(self):
        self.state = Boss.WALK

        px = world.player.x
        self.dir = -1 if px > self.x else 1

        self.x += -self.dir * self.speed * game_framework.frame_time
        self.x = clamp(50, self.x, 1230)

        if abs(px - self.x) < 120:
            pass

        return BehaviorTree.RUNNING

    def action_idle(self):
        self.state = Boss.IDLE
        return BehaviorTree.SUCCESS

    def is_attacking(self):
        if self.state == Boss.ATTACK:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def build_behavior_tree(self):
        c0 = Condition("공격 중인가?", self.is_attacking)

        c1 = Condition("공격 가능?", self.attack_ready)
        c2 = Condition("플레이어가 가까운가?", self.player_near, Boss.ATTACK_RANGE)
        a1 = Action("공격 시작", self.action_attack)
        attack_seq = Sequence("공격", c1,c2, a1)

        c3 = Condition("플레이어 감지?", self.player_near, Boss.ATTACK_RANGE + 200)
        a2 = Action("추적", self.action_chase_player)
        chase_seq = Sequence("추적", c3,a2)

        a4 = Action("대기", self.action_idle)

        root = Selector("보스 루트", c0, attack_seq, chase_seq, a4)

        self.bt = BehaviorTree(root)


    def update(self, frame_time):

        if self.is_dead:
            if int(self.frame) < Boss.DIE_FRAME_COUNT - 1:
                self.frame += self.frame_per_sec * frame_time
            else:
                self.frame = Boss.DIE_FRAME_COUNT - 1
            return

        if world.player is None or world.player.hp <= 0:
            self.state = Boss.IDLE
            self.frame = (self.frame + self.frame_per_sec * frame_time) % Boss.IDLE_FRAME_COUNT
            return

        if self.attack_cool > 0:
            self.attack_cool -= frame_time

        if self.hit_timer > 0:
            self.hit_timer -= frame_time

        self.bt.run()

        if self.state == Boss.IDLE:
            self.frame = (self.frame + self.frame_per_sec * frame_time) % Boss.IDLE_FRAME_COUNT

        elif self.state == Boss.WALK:
            self.frame = (self.frame + self.frame_per_sec * frame_time) % Boss.WALK_FRAME_COUNT

        elif self.state == Boss.ATTACK:
            if self.hp < self.max_hp / 2:
                self.frame += self.frame_per_sec * frame_time * 2
            else:
                self.frame += self.frame_per_sec * frame_time
            current_frame = int(self.frame)

            if 10 <= current_frame <= 13 and not self.attack_processed:
                if Boss.boss_attack_sound is not None:
                    Boss.boss_attack_sound.play()
                if world.player and abs(world.player.x - self.x) < 250:

                    if world.player.state_machine.current_state is world.player.ROLL:
                        pass
                    elif world.player.roll_god > 0:
                        pass
                    elif world.player.god_timer > 0:
                        pass
                    else:
                        world.player.take_hit(self.damage)
                self.attack_processed = True

            if self.frame >= Boss.ATTACK_FRAME_COUNT:
                self.state = Boss.IDLE
                self.frame = 0.0
                self.attack_processed = False


    def draw(self):
        if self.is_dead:
            row = Boss.DEAD_ROW
            frame_count = Boss.DIE_FRAME_COUNT
        elif self.state == Boss.IDLE:
            row = Boss.IDLE_ROW
            frame_count = Boss.IDLE_FRAME_COUNT
        elif self.state == Boss.WALK:
            row = Boss.WALK_ROW
            frame_count = Boss.WALK_FRAME_COUNT
        elif self.state == Boss.ATTACK:
            row = Boss.ATTACK_ROW
            frame_count = Boss.ATTACK_FRAME_COUNT
        else:
            row = Boss.IDLE_ROW
            frame_count = Boss.IDLE_FRAME_COUNT

        idx = int(self.frame) % frame_count
        x_clip = idx * self.w
        y_clip = row * self.h

        draw_w = self.w * 3
        draw_h = self.h * 3
        draw_y = self.y + draw_h / 2

        if self.dir == 1:
            self.image.clip_draw(x_clip, y_clip, self.w, self.h, self.x, draw_y, draw_w, draw_h)
        else:
            self.image.clip_composite_draw(x_clip, y_clip, self.w, self.h, 0, 'h', self.x, draw_y, draw_w, draw_h)

        # draw_rectangle(*self.get_bb()) # 충돌 박스 디버깅용

        self.draw_hp_bar()

    def get_bb(self):
        return self.x - BOSS_BB_W, self.y, self.x + BOSS_BB_W, self.y + BOSS_BB_H

    def handle_collision(self, group, other):
        if group == 'player:attack':
            self.take_hit(other.damage)

    def take_hit(self, damage):
        if self.hit_timer > 0 or self.is_dead:
            return

        self.hit_timer = 0.3
        self.hp -= damage

        if not self.rage and self.hp < self.max_hp / 2:
            self.rage = True
            if Boss.boss_rage_sound is not None:
                Boss.boss_rage_sound.play()

        if Boss.boss_hit_sound is not None:
            Boss.boss_hit_sound.play()

        world.add_object(DamageTextAni(self.x, self.y + 280, damage), 3)

        if self.hp <= 0:
            self.is_dead = True
            if Boss.boss_dead_sound is not None:
                Boss.boss_dead_sound.play()
            self.state = Boss.DEAD
            self.frame = 0.0

            try:
                world.monsters.remove(self)
            except ValueError:
                pass

    def draw_hp_bar(self):
        bar_w = 128
        bar_h = 32
        x = self.x
        y = self.y + 270

        ratio = max(self.hp / self.max_hp, 0)
        fill_w = int(bar_w * ratio)

        self.hp_bar.clip_draw(0, 0,fill_w, bar_h,x - (bar_w // 2) + fill_w / 2,y,fill_w * 2.5, bar_h * 3)