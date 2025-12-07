from pico2d import *
import world
from text_ani import DamageTextAni


BOSS_W = 288
BOSS_H = 160

BOSS_BB_W = 120
BOSS_BB_H = 250


class Boss:
    image = None

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

    def __init__(self, x, y):
        if Boss.image is None:
            Boss.image = load_image('Boss.png')

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

        self.hit_timer = 0.0
        self.is_dead = False

        self.w, self.h = BOSS_W, BOSS_H
        self.ground_y = world.ground_y

    def update(self, frame_time):

        if self.is_dead:
            if int(self.frame) < Boss.DIE_FRAME_COUNT - 1:
                self.frame += self.frame_per_sec * frame_time
            else:
                self.frame = Boss.DIE_FRAME_COUNT - 1
            return

        if world.player and world.player.hp <= 0:
            self.state = Boss.IDLE
            self.frame = (self.frame + self.frame_per_sec * frame_time) % Boss.IDLE_FRAME_COUNT
            return

        if self.state == Boss.HIT:
            self.frame += self.frame_per_sec * frame_time * 1.5
            if self.frame >= Boss.HIT_FRAME_COUNT:
                self.state = Boss.IDLE
                self.frame = 0.0

        elif self.state == Boss.ATTACK:
            self.frame += self.frame_per_sec * frame_time

            current_frame = int(self.frame)

            if 10 <= current_frame <= 13 and not self.attack_processed:

                if world.player and abs(world.player.x - self.x) < 200:
                    world.player.take_hit(self.damage)

                    self.attack_processed = True

            if self.frame >= Boss.ATTACK_FRAME_COUNT:
                self.state = Boss.IDLE
                self.frame = 0.0
                self.attack_processed = False

        else:
            if world.player:
                dx = world.player.x - self.x
                distance = abs(dx)

                if dx < 0:
                    self.dir = 1
                else:
                    self.dir = -1

                attack_range = 150

                if distance > attack_range:
                    self.state = Boss.WALK
                    self.x += -self.dir * self.speed * frame_time

                    self.x = clamp(50, self.x, 1230)
                else:
                    self.state = Boss.ATTACK
                    self.frame = 0.0
                    self.attack_processed = False

        if self.state == Boss.IDLE:
            self.frame = (self.frame + self.frame_per_sec * frame_time) % Boss.IDLE_FRAME_COUNT

        elif self.state == Boss.WALK:
            self.frame = (self.frame + self.frame_per_sec * frame_time) % Boss.WALK_FRAME_COUNT

        if self.hit_timer > 0:
            self.hit_timer -= frame_time

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
        elif self.state == Boss.HIT:
            row = Boss.HIT_ROW
            frame_count = Boss.HIT_FRAME_COUNT
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

        draw_rectangle(self.x - 150, self.y + 250, self.x + 150, self.y + 265)
        hp_width = 300 * (self.hp / self.max_hp)
        draw_rectangle(self.x - 150, self.y + 250, self.x - 150 + hp_width, self.y + 265)
        draw_rectangle(*self.get_bb()) # 충돌 박스 디버깅용

    def get_bb(self):
        return self.x - BOSS_BB_W, self.y, self.x + BOSS_BB_W, self.y + BOSS_BB_H

    def handle_collision(self, group, other):

        if group == 'player:attack':
            self.take_hit(other.damage)
            return

    def take_hit(self, damage):
        if self.hit_timer > 0 or self.is_dead:
            return

        self.hit_timer = 0.3
        self.hp -= damage

        world.add_object(DamageTextAni(self.x, self.y + 280, damage), 3)

        if self.hp <= 0:
            self.is_dead = True
            self.state = Boss.DEAD
            self.frame = 0.0

            try:
                world.monsters.remove(self)
            except ValueError:
                pass
            return
        self.state = Boss.HIT
        self.frame = 0.0
        self.x += self.dir * 10