from pico2d import *
import world
from background import Background, Blacksmith, Ground, House, Portal
from player import Player
from NPC import Npc
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
        else: world.player.handle_event(event)
            
open_canvas(1280, 720)


def reset_world():
    global running
    running = True

    background = Background()
    ground = Ground()
    blacksmith = Blacksmith()
    house = House()
    portal = Portal()
    npc = Npc()
    player = Player()
    gametime = GameTime()

    world.player = player
    world.gametime = gametime

    world.add_object(background, 0)
    world.add_object(ground, 1)
    world.add_object(portal, 0)
    world.add_object(blacksmith, 0)
    world.add_object(house, 1)
    world.add_object(npc, 2)
    world.add_object(player, 3)
    world.add_object(gametime, 3)

    world.crops = []
    pass


reset_world()

prev_time = get_time()

def update_world():
    global prev_time
    now = get_time()
    frame_time = now - prev_time
    prev_time = now

    world.update(frame_time)

    for crop in world.crops:
        crop.update(frame_time)
    pass


def render_world():
    clear_canvas()
    world.render()
    for crop in world.crops:
        crop.draw()
    update_canvas()
    pass


while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)



close_canvas()

