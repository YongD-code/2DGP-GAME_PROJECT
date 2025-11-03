from pico2d import *
import game_framework
import world
import title_mode

def init():
    global background
    background = load_image('dungeon_1stage.png')

def finish():
    world.clear()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)

def update():
    pass

def draw():
    clear_canvas()
    background.draw(640, 360)
    update_canvas()

def pause():
    pass

def resume():
    pass
