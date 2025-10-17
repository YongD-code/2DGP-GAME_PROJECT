from pico2d import *
from background import Background
from player import Player
from background import Blacksmith
from background import Ground

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else: player.handle_event(event)
            
            
open_canvas(1280, 720)


def reset_world():
    global running, background,player,blacksmith,ground
    running = True
    background = Background()
    ground = Ground()
    blacksmith = Blacksmith()
    player = Player()
    pass


reset_world()


def update_world():
    #background.update()
    blacksmith.update()
    player.update()
    pass


def render_world():
    clear_canvas()
    background.draw()
    ground.draw()
    blacksmith.draw()
    player.draw()
    update_canvas()
    pass


while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)



close_canvas()

