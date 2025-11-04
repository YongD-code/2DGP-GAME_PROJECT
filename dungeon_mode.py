from pico2d import *
import game_framework
import world
from player import Player
import GAME_PROJECT

def init():
    global background, player
    background = load_image('dungeon_1stage.png')

    world.clear()

    player = Player()
    player.x, player.y = 110,180
    world.player = player
    world.set_ground_y(180)
    world.add_object(player, 1)
    if world.gametime is not None:
        world.add_object(world.gametime, 3)

def finish():
    world.clear()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
            game_framework.change_mode(GAME_PROJECT)
        else:
            world.player.handle_event(e)

def update():
    frame_time = 0.05
    world.update(frame_time)
    delay(frame_time)

def draw():
    clear_canvas()
    background.draw(640, 360)
    world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
