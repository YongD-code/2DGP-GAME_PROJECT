from pico2d import *
import random

class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(640, 360)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
            
            
open_canvas(1280, 720)


def reset_world():
    global running, background
    running = True
    background = Background()
    pass


reset_world()


def update_world():
    pass


def render_world():
    clear_canvas()
    background.draw()
    update_canvas()
    pass


while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)



close_canvas()

