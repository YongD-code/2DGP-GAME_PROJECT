from pico2d import *
import math
import random
import world


SLIME_BW   = 22.0
SLIME_BH   = 20.0
SLIME_BX = 0.0
SLIME_BY = -10.0



class Slime:
    DETECT_RADIUS   = 260.0
    STOP_DIST       = 24.0
    IDLE_FRAME_TIME = 0.15
    MOVE_FRAME_TIME = 0.10
    MOVE_SPEED      = 110.0
    hp_bar = load_image('hp.png')
    slime_hit_sound = None
    def __init__(self, x, y, color='blue'):
        self.blue_slime  = load_image('blue_slime.png')
        self.green_slime = load_image('green_slime.png')
        self.red_slime   = load_image('red_slime.png')

        if not Slime.slime_hit_sound:
            Slime.slime_hit_sound = load_wav('sound/slime.wav')
            Slime.slime_hit_sound.set_volume(32)

        self.hp = 40
        self.max_hp = 40
        self.hit_timer = 0.0

        self.cols = 7
        self.rows = 6
        self.w = 128 // self.cols
        self.h = 20

        self.x, self.y = x, y
        self.dir = random.choice([-1, 1])
        self.speed = Slime.MOVE_SPEED
        self.frame = 0
        self.action = 0
        self.time_acc = 0.0

        self.idle_row = 6
        self.idle_frame_count = 4
        self.move_row = 5
        self.move_frame_count = 5
        self.hit_row = 3
        self.hit_frame_count = 3
        self.death_row = 2
        self.death_frame_count = 5
        self.is_hit = False
        self.hit_anim_timer = 0.0
        self.hit_anim_duration = 0.25
        self.dead_ani = False
        self.death_anim_timer = 0.0

        self.sheet = None
        self.set_color(color)

    def set_color(self, color: str):
        c = (color or '').lower()
        if c == 'green':
            self.sheet = self.green_slime
        elif c == 'red':
            self.sheet = self.red_slime
        else:
            self.sheet = self.blue_slime

    def update(self, frame_time):
        if self.dead_ani:
            self.death_anim_timer += frame_time
            if self.death_anim_timer >= 0.08:
                self.frame += 1
                self.death_anim_timer = 0.0

            if self.frame >= self.death_frame_count:
                import world
                world.remove_object(self)
            return

        try:
            from world import player, left_boundary, right_boundary
        except ImportError:
            player = None
            left_boundary, right_boundary = 0, 999999

        if player is not None:
            same_floor = abs(player.y - self.y - 95) <= 5
            if same_floor:
                dx = player.x - self.x
                if abs(dx) <= Slime.DETECT_RADIUS:
                    self.action = 1
                    if abs(dx) > Slime.STOP_DIST:
                        self.dir = 1 if dx > 0 else -1
                        self.x += self.dir * self.speed * frame_time
                else:
                    self.action = 0
            else:
                self.action = 0
        else:
            self.action = 0

        if self.x < left_boundary + 40:
            self.x = left_boundary + 40
            self.dir = 1
        elif self.x > right_boundary - 40:
            self.x = right_boundary - 40
            self.dir = -1

        self.time_acc += frame_time
        if self.action == 0:
            if self.time_acc >= Slime.IDLE_FRAME_TIME:
                self.frame = (self.frame + 1) % self.idle_frame_count
                self.time_acc = 0.0
        else:
            if self.time_acc >= Slime.MOVE_FRAME_TIME:
                self.frame = (self.frame + 1) % self.move_frame_count
                self.time_acc = 0.0

        if getattr(self, 'hit_timer', 0) > 0:
            self.hit_timer -= frame_time

        if self.is_hit:
            self.hit_anim_timer += frame_time
            if self.hit_anim_timer >= 0.05:
                self.frame = (self.frame + 1) % self.hit_frame_count
                self.hit_anim_timer = 0.0

            if self.hit_timer <= 0:
                self.is_hit = False

    def draw(self):
        if self.dead_ani:
            row = self.death_row
            frame_count = self.death_frame_count
        elif self.is_hit:
            row = self.hit_row
            frame_count = self.hit_frame_count
        else:
            if self.action == 0:
                row = self.idle_row
                frame_count = self.idle_frame_count
            else:
                row = self.move_row
                frame_count = self.move_frame_count

        idx = int(self.frame) % frame_count
        x_clip = idx * self.w
        y_clip = (self.rows + row) * self.h

        draw_w = self.w * 3
        draw_h = self.h * 3

        if self.dir == 1:
            self.sheet.clip_draw(x_clip, y_clip, self.w, self.h,self.x, self.y, draw_w, draw_h)
        else:
            self.sheet.clip_composite_draw(x_clip, y_clip, self.w, self.h, 0, 'h', self.x, self.y, draw_w, draw_h)

        draw_rectangle(*self.get_bb())
        self.draw_hp_bar()

    def get_bb(self):
        cx = self.x + SLIME_BX
        cy = self.y + SLIME_BY
        return cx - SLIME_BW, cy - SLIME_BH ,cx + SLIME_BW, cy + SLIME_BH

    def handle_collision(self, group, other):
        if group == 'player:attack':
            self.take_hit()
            return

    def take_hit(self):
        import world
        if getattr(self, 'hit_timer', 0) > 0:
            return

        self.hit_timer = 0.3
        damage = world.player.damage
        self.hp -= damage

        if Slime.slime_hit_sound is not None:
            Slime.slime_hit_sound.play()

        from text_ani import DamageTextAni

        world.add_object(DamageTextAni(self.x, self.y + 30,damage), 3)

        if self.hp <= 0:
            self.dead_ani = True
            self.death_anim_timer = 0.0
            self.frame = 0

            try:
                world.monsters.remove(self)
            except ValueError:
                pass

            world.quest_manage.add_progress("quest_slime", 1)
            return

        self.is_hit = True
        self.hit_anim_timer = 0.0
        self.frame = 0

        if self.hp <= 0:
            import world
            world.remove_object(self)
        else:
            self.x += -self.dir * 20

    def draw_hp_bar(self):
        bar_w = 128
        bar_h = 32
        x = self.x
        y = self.y + 25

        ratio = max(self.hp / self.max_hp, 0)
        fill_w = int(bar_w * ratio)

        self.hp_bar.clip_draw(0, 0,fill_w, bar_h,x - (bar_w // 2) + fill_w / 2,y,fill_w * 0.5, bar_h)