from pico2d import load_image


class Run:
    def enter(player):
        player.image = load_image('_Run.png')
        player.frame = 0

    def exit(player):
        pass

    def do(player):
        player.frame = (player.frame + 1) % 10
        player.x += 5
        if player.x > 1160:
            player.dir = 0
        if player.x < 120:
            player.dir = 0

    def draw(player):
        player.image.clip_draw(player.frame, 0, player.w, player.h, player.x, player.y, player.w * 3, player.h * 3)
