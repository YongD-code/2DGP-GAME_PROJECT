from pico2d import *
import world
from background import Background, Blacksmith, Ground, House, Portal,InventoryIcon
from player import Player
from NPC import Npc
from time_clock import GameTime
from inventory import Inventory
from crop import Crop
import quest_manage
import dialogue
import game_framework
import title_mode
from ui import GameUI
from upgrade import Upgrade
running = True
prev_time = 0.0

def init():
    global running, prev_time,gametime
    world.dungeon_map = None
    if world.player is None:
        player = Player()
        world.player = player
    else:
        player = world.player
        player.x, player.y = 80, 228
        player.hp = player.max_hp
        player.dead_ani = False
        player.state_machine.change_state(player.IDLE)

    running = True
    prev_time = get_time()

    background = Background()
    ground = Ground()
    blacksmith = Blacksmith()
    house = House()
    portal = Portal()
    npc = Npc()
    inventoryicon = InventoryIcon()

    world.ground = ground
    world.portal = portal
    world.npc = npc
    world.inventory_icon = inventoryicon
    if world.inventory is None:
        world.inventory = Inventory()
        world.inventory.quickslot_scale = 1.0
        world.inventory.quickslot_ui_scale = 1.0

        seed_index = world.inventory.add_item("seed_corn")
        world.inventory.items[seed_index]["count"] = 5

        seed_index = world.inventory.add_item("seed_pumpkin")
        world.inventory.items[seed_index]["count"] = 5

        seed_index = world.inventory.add_item("seed_potato")
        world.inventory.items[seed_index]["count"] = 5

        seed_index = world.inventory.add_item("seed_strawberry")
        world.inventory.items[seed_index]["count"] = 5
    else:
        world.inventory.quickslot_scale = 1.0
        world.inventory.quickslot_ui_scale = 1.0

    world.blacksmith = blacksmith

    if world.quest_manage is None:
        world.quest_manage = quest_manage.QuestManage()

    world.ui = GameUI()

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


    world.active_upgrade = None

    world.inventory.quickslot_offset_y = -310
    world.inventory.quickslot_R_offset_x = 225
    world.inventory.quickslot_R_offset_y = 10
    world.inventory.gap = 54
    world.inventory.update_quickslot_positions()

    if hasattr(world, "crops"):
        for crop in world.crops:
            world.add_object(crop, 2)
    pass


def finish():
    world.clear()
    pass

def handle_events():
    global running

    events = get_events()
    for event in events:
        if hasattr(world, "active_upgrade") and world.active_upgrade:
            if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
                world.active_upgrade.upgrade()
                if not world.active_upgrade.active:
                    world.active_upgrade = None
                return
        if hasattr(world, "active_dialogue") and world.active_dialogue:
            if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
                if not world.active_dialogue.next():
                    world.active_dialogue = None
                return True

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_f:
            if world.npc.can_talk():
                world.player.handle_event(event)
                return
            if world.blacksmith and world.blacksmith.in_range(world.player):
                world.active_upgrade = Upgrade()
                return

        else:
            if not world.inventory.visible:
                world.player.handle_event(event)


def update():
    global prev_time

    world.update(game_framework.frame_time)
    for crop in world.crops:
        crop.update(game_framework.frame_time)

    if hasattr(world, 'ui'):
        world.ui.update(game_framework.frame_time)

    if hasattr(world, "active_dialogue") and world.active_dialogue:
        world.active_dialogue.update = lambda ft: None
        return

    # delay(0.04)
    pass


def draw():
    clear_canvas()
    for crop in world.crops:
        crop.draw()
    world.render()
    if hasattr(world, 'inventory'):
        world.inventory.draw()

    if hasattr(world, "active_dialogue") and world.active_dialogue:
        world.active_dialogue.draw()

    if hasattr(world, 'ui'):
        world.ui.draw_hp(world.player.hp)
        world.ui.draw_gold(world.gold)

    if hasattr(world, "active_upgrade") and world.active_upgrade:
        world.active_upgrade.draw()
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass
