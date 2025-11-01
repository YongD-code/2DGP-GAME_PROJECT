from pico2d import *
import world
from background import Background, Blacksmith, Ground, House, Portal
from player import Player
from NPC import Npc
from time_clock import GameTime
from crop import Crop

import game_framework
import title_mode

running = True
prev_time = 0.0

def init():
    global running, prev_time

    running = True
    prev_time = get_time()

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


def finish():
    world.clear()
    pass

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            world.player.handle_event(event)
    pass


def update():
    global prev_time

    now = get_time()
    frame_time = now - prev_time
    prev_time = now

    world.update(frame_time)

    for crop in world.crops:
        crop.update(frame_time)
    pass


def draw():
    clear_canvas()
    world.render()

    for crop in world.crops:
        crop.draw()

    update_canvas()
    pass


def pause():
    pass


def resume():
    pass
