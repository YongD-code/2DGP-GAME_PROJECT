from pico2d import *
import random

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
            
            
open_canvas()


def reset_world():
    pass


reset_world()


def update_world():
    pass


def render_world():
    pass


while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)



close_canvas()

