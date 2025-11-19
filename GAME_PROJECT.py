from pico2d import *
import world
from background import Background, Blacksmith, Ground, House, Portal,InventoryIcon
from player import Player
from NPC import Npc
from time_clock import GameTime
from inventory import Inventory
from crop import Crop

import game_framework
import title_mode

running = True
prev_time = 0.0

def init():
    global running, prev_time,gametime

    running = True
    prev_time = get_time()

    background = Background()
    ground = Ground()
    blacksmith = Blacksmith()
    house = House()
    portal = Portal()
    npc = Npc()
    player = Player()
    inventoryicon = InventoryIcon()
    inventory = Inventory()

    world.player = player
    world.ground = ground
    world.portal = portal
    world.inventory_icon = inventoryicon
    world.inventory = inventory
    seed_index = world.inventory.add_item("seed_corn")
    world.inventory.items[seed_index]["count"] = 5

    seed_index = world.inventory.add_item("seed_pumpkin")
    world.inventory.items[seed_index]["count"] = 5

    seed_index = world.inventory.add_item("seed_potato")
    world.inventory.items[seed_index]["count"] = 5

    seed_index = world.inventory.add_item("seed_strawberry")
    world.inventory.items[seed_index]["count"] = 5

    world.set_ground_y(228)
    world.set_boundary(30,1250)

    world.add_object(background, 0)
    world.add_object(ground, 1)
    world.add_object(portal, 0)
    world.add_object(blacksmith, 0)
    world.add_object(house, 1)
    world.add_object(inventoryicon,1)
    world.add_object(npc, 2)
    world.add_object(player, 3)

    if world.gametime is None:
        gametime = GameTime()
        world.gametime = gametime
        world.add_object(gametime, 3)
    else:
        gametime = world.gametime
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
        elif hasattr(world, 'inventory_icon') and world.inventory_icon.handle_event(event):
            world.inventory.toggle()
            return

        elif hasattr(world, 'inventory') and world.inventory.handle_event(event):
            return

        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            world.inventory.toggle()
            return
        else:
            if not world.inventory.visible:
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

    delay(0.04)
    pass


def draw():
    clear_canvas()
    for crop in world.crops:
        crop.draw()
    world.render()
    if hasattr(world, 'inventory'):
        world.inventory.draw()
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass
