from pico2d import *
from background import Background
from player import Player
from background import Blacksmith
from background import Ground
from background import Portal
from NPC import Npc
from background import House
from time_clock import GameTime
from crop import Crop

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
    global running, background,player,blacksmith,ground,portal,npc,house,gametime,crops
    running = True
    background = Background()
    portal = Portal()
    ground = Ground()
    blacksmith = Blacksmith()
    house = House()
    npc = Npc()
    crops = []
    player = Player()
    gametime = GameTime()
    pass


reset_world()

prev_time = get_time()

def update_world():
    global prev_time
    now = get_time()
    frame_time = now - prev_time
    prev_time = now

    #background.update()
    portal.update()
    blacksmith.update()
    house.update()
    player.update()
    npc.update(player.x)
    gametime.update(frame_time)

    for crop in crops:
        crop.update(frame_time)
    pass


def render_world():
    clear_canvas()
    background.draw()
    portal.draw()
    blacksmith.draw()
    ground.draw()
    house.draw()
    npc.draw()
    for crop in crops:
        crop.draw()
    player.draw()
    gametime.draw()
    update_canvas()
    pass


while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)



close_canvas()

