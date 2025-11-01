from pico2d import *
import game_framework
import GAME_PROJECT

image = None

def init():
    global image
    image = load_image('Gamestart_framework.png')
    pass

def finish():
    global image
    del image
    pass

def update():
    pass

def draw():
    clear_canvas()
    image.draw(640, 360)
    update_canvas()
    pass

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(GAME_PROJECT)
    pass


def pause():
    pass

def resume():
    pass
