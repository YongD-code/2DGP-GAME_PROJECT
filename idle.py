from pico2d import *

class Idle:
    def enter(player):
        player.image = load_image('_Idle.png')
        player.frame = 0

    def exit(player):
        pass

    def update(player):
        player.frame = (player.frame + 1) % 10

    def draw(player):
        player.image.clip_draw(player.frame * player.w, 0, player.w, player.h, player.x, player.y, player.w * 3,player.h * 3)