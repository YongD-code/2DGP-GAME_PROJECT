from pico2d import *
import random

SKELETON_BW   = 26.0
SKELETON_BH   = 40.0
SKELETON_BX = 0.0
SKELETON_BY = 0.0

class Skeleton:

    DETECT_RADIUS   = 260.0
    STOP_DIST       = 24.0
    IDLE_FRAME_TIME = 0.15
    MOVE_FRAME_TIME = 0.10
    MOVE_SPEED      = 110.0

    def __init__(self,x,y):
        self.image = load_image('skeleton.png')

        self.hp = 50
        self.hit_timer = 0.0


        self.cols = 7
        self.rows = 6
        self.w = 18
        self.h = 17

        self.x, self.y = x, y
        self.dir = random.choice([-1, 1])
        self.speed = Skeleton.MOVE_SPEED
        self.frame = 0
        self.action = 0
        self.time_acc = 0.0

        self.idle_row = 6
        self.idle_frame_count = 4
        self.move_row = 5
        self.move_frame_count = 4
        self.hit_row = 3
        self.hit_frame_count = 3
        self.is_hit = False
        self.hit_anim_timer = 0.0
        self.death_row = 2
        self.death_frame_count = 6
        self.is_dead = False
        self.death_anim_timer = 0.0

    def update(self, frame_time):
        if self.is_dead:
            self.death_anim_timer += frame_time
            if self.death_anim_timer >= 0.08:
                self.frame += 1
                self.death_anim_timer = 0.0

            if self.frame >= self.death_frame_count:
                import world
                world.remove_object(self)
            return
        if self.is_hit:
            self.hit_anim_timer += frame_time
            if self.hit_anim_timer >= 0.05:
                self.frame = (self.frame + 1) % self.hit_frame_count
                self.hit_anim_timer = 0.0

            if self.hit_timer <= 0:
                self.is_hit = False
        try:
            from world import player, left_boundary, right_boundary
        except ImportError:
            player = None
            left_boundary, right_boundary = 0, 999999

        if player is not None:
            same_floor = abs(player.y - self.y - 80) <= 5
            if same_floor:
                dx = player.x - self.x
                if abs(dx) <= Skeleton.DETECT_RADIUS:
                    self.action = 1
                    if abs(dx) > Skeleton.STOP_DIST:
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
            if self.time_acc >= Skeleton.IDLE_FRAME_TIME:
                self.frame = (self.frame + 1) % self.idle_frame_count
                self.time_acc = 0.0
        else:
            if self.time_acc >= Skeleton.MOVE_FRAME_TIME:
                self.frame = (self.frame + 1) % self.move_frame_count
                self.time_acc = 0.0

        if getattr(self, 'hit_timer', 0) > 0:
            self.hit_timer -= frame_time

    def draw(self):
        if self.is_dead:
            row = self.death_row
            frame_count = self.death_frame_count
            y_offset = 10
        elif self.is_hit:
            row = self.hit_row
            frame_count = self.hit_frame_count
            y_offset = 10
        else:
            if self.action == 0:
                row = self.idle_row
                frame_count = self.idle_frame_count
                y_offset = 0
            else:
                row = self.move_row
                frame_count = self.move_frame_count
                y_offset = 5

        idx = int(self.frame) % frame_count
        x_clip = idx * self.w
        y_clip = row * self.h

        draw_w = self.w * 3
        draw_h = self.h * 3

        if self.dir == 1:
            self.image.clip_draw(x_clip, y_clip, self.w, self.h,self.x, self.y+y_offset, draw_w*2, draw_h*2)
        else:
            self.image.clip_composite_draw(x_clip, y_clip, self.w, self.h, 0, 'h', self.x, self.y+y_offset, draw_w*2, draw_h*2)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        cx = self.x + SKELETON_BX
        cy = self.y + SKELETON_BY
        return cx - SKELETON_BW, cy - SKELETON_BH , cx + SKELETON_BW, cy + SKELETON_BH

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

        from text_ani import DamageTextAni
        world.add_object(DamageTextAni(self.x, self.y + 30, damage), 3)

        if self.hp <= 0:
            self.is_dead = True
            self.frame = 0
            self.death_anim_timer = 0.0

            try:
                world.monsters.remove(self)
            except ValueError:
                pass

            return

        self.is_hit = True
        self.frame = 0
        self.hit_anim_timer = 0.0

        if self.hp <= 0:
            import world
            world.remove_object(self)
        else:
            self.x += -self.dir * 25