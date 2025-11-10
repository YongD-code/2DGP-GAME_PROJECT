from pico2d import *
import world, game_framework

class Hit:
    def __init__(self, player):
        self.player = player
        self.hit_image = load_image('hit.png')
        self.image = self.hit_image
        self.timer = 0.0
        self.knock_timer = 0.0
        self.knock_dir = 0

    def enter(self, event):
        self.image = self.hit_image
        self.timer = 0.30
        self.knock_timer = 0.1
        self.knock_dir = -self.player.dir

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time

        if self.knock_timer > 0.0:
            self.player.x += self.knock_dir * 200.0 * dt
            self.knock_timer -= dt

        self.timer -= dt
        if self.timer <= 0.0:
            if self.player.right_input or self.player.left_input:
                self.player.state_machine.change_state(self.player.RUN)
            else:
                self.player.state_machine.change_state(self.player.IDLE)

        if self.player.x > world.right_boundary:
            self.player.x = world.right_boundary
        if self.player.x < world.left_boundary:
            self.player.x = world.left_boundary

    def draw(self):
        if self.player.dir == 1:
            self.image.draw(self.player.x, self.player.y,self.player.w * 3, self.player.h * 3)
        else:
            self.image.composite_draw(0, 'h', self.player.x, self.player.y,self.player.w * 3, self.player.h * 3)

