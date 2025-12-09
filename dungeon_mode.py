from pico2d import *
import game_framework
import world
from player import Player
import GAME_PROJECT
from slime import Slime
from dungeon_tile import DungeonMap
import random
from background import DungeonPortal
from skeleton import Skeleton
from goblin import Goblin
from upgrade import Upgrade
from boss import Boss

stage_num = 1
dungeon_bgm = None
boss_bgm = None
current_bgm = None

def init(stage = None):
    global background, player,dungeon_map, stage_num,dungeon_bgm, boss_bgm, current_bgm
    if hasattr(world, "spawned_portal"):
        del world.spawned_portal
    world_damage = getattr(world.player, "damage", 1)
    world_damage_level = getattr(world.player, "damage_level", 0)
    world_hp = world.player.hp if world.player else None
    world_gold = getattr(world, "gold", 0)
    world_inventory_items = None
    world_inventory_slots = None
    world_quickslots = None

    if stage is not None:
        stage_num = stage
    background = load_image('dungeon_bg.png')

    if dungeon_bgm is None:
        dungeon_bgm = load_music('sound/dungeon.mp3')
        dungeon_bgm.set_volume(32)

    if boss_bgm is None:
        boss_bgm = load_music('sound/boss.mp3')
        boss_bgm.set_volume(32)

    if stage_num == 4:
        if current_bgm != 'boss':
            if current_bgm == 'dungeon':
                dungeon_bgm.stop()
            boss_bgm.repeat_play()
            current_bgm = 'boss'
    else:
        if current_bgm != 'dungeon':
            if current_bgm == 'boss':
                boss_bgm.stop()
            dungeon_bgm.repeat_play()
            current_bgm = 'dungeon'

    world.clear()

    player = world.player
    player.x, player.y = 110,180

    if world_hp is not None:
        player.hp = world_hp
    player.damage = world_damage
    player.damage_level = world_damage_level

    world.gold = world_gold

    if world_inventory_items is not None:
        world.inventory.items = [item.copy() for item in world_inventory_items]
        world.inventory.slots = [slot.copy() for slot in world_inventory_slots]
        world.inventory.quickslots = world_quickslots.copy()

    world.set_ground_y(180)
    world.set_boundary(110, 1170)
    world.add_object(player, 2)
    world.monsters = []
    world.inventory.quickslot_scale = 0.7
    world.inventory.quickslot_ui_scale = 0.7
    world.inventory.quickslot_offset_y = -330
    world.inventory.gap = 38
    world.inventory.quickslot_R_offset_x = 158
    world.inventory.quickslot_R_offset_y = 8
    world.inventory.update_quickslot_positions()

    if world.gametime is not None:
        world.add_object(world.gametime, 3)

    if stage_num == 1:
        dungeon_map = DungeonMap(stage_num)
        world.dungeon_map = dungeon_map
        world.add_object(dungeon_map,0)

        slime_list = [Slime(random.randint(500,850), 85,'blue'),
                      Slime(random.randint(900,1220), 85,'red'),
                      Slime(random.randint(100,300), 520,'green'),
                      Slime(random.randint(350, 550), 520, 'red'),
                      Slime(random.randint(1000,1220), 390,'blue'),
                      Slime(random.randint(200,350),290,'red'),
                      Slime(random.randint(400, 700), 290, 'green')
                      ]
        for s in slime_list:
            world.add_object(s, 1)
            world.monsters.append(s)
        for t in world.dungeon_map.get_tiles():
            world.add_collision_pair('player:tile', world.player, t)

        for s in slime_list:
            world.add_collision_pair('player:slime', world.player, s)
        #
        # portal = DungeonPortal()
        # world.add_object(portal, 0)
        # world.add_collision_pair('player:portal', player, portal)

    elif stage_num == 2:
        dungeon_map = DungeonMap(stage_num)
        world.dungeon_map = dungeon_map
        world.add_object(dungeon_map,0)

        skeleton_list = [Skeleton(random.randint(500,850), 95),
                      Skeleton(random.randint(900,1220), 95),
                      Skeleton(random.randint(1000,1220), 500),
                      Skeleton(random.randint(200,350),300),
                      Skeleton(random.randint(400, 700), 300)
                      ]
        for s in skeleton_list:
            world.add_object(s, 1)
            world.monsters.append(s)

        for t in world.dungeon_map.get_tiles():
            world.add_collision_pair('player:tile', world.player, t)

        for s in skeleton_list:
            world.add_collision_pair('player:skeleton', world.player, s)

        # portal = DungeonPortal()
        # world.add_object(portal, 0)
        # world.add_collision_pair('player:portal', player, portal)

    elif stage_num == 3:
        dungeon_map = DungeonMap(stage_num)
        world.dungeon_map = dungeon_map
        world.add_object(dungeon_map,0)

        goblin_list = [Goblin(random.randint(500,850), 95),
                      Goblin(random.randint(900,1220), 95),
                      Goblin(random.randint(1000,1220), 500),
                      Goblin(random.randint(200,350),280),
                      Goblin(random.randint(500, 800), 390)
                      ]
        for s in goblin_list:
            world.add_object(s, 1)
            world.monsters.append(s)

        for t in world.dungeon_map.get_tiles():
            world.add_collision_pair('player:tile', world.player, t)

        for g in goblin_list:
            world.add_collision_pair('player:goblin', world.player, g)

        # portal = DungeonPortal()
        # world.add_object(portal, 0)
        # world.add_collision_pair('player:portal', player, portal)
    elif stage_num == 4:
        dungeon_map = DungeonMap(stage_num)
        world.dungeon_map = dungeon_map
        world.add_object(dungeon_map, 0)

        boss_list = [Boss(1000, 55)]

        for b in boss_list:
            world.add_object(b, 1)
            world.monsters.append(b)

        for b in boss_list:
            world.add_collision_pair('player:boss', world.player, b)


def finish():
    global dungeon_bgm, boss_bgm, current_bgm
    if dungeon_bgm is not None:
        dungeon_bgm.stop()
    if boss_bgm is not None:
        boss_bgm.stop()
    current_bgm = None
    world.clear()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()

        if e.type == SDL_KEYDOWN and e.key == SDLK_s:
            return
        if hasattr(world, 'inventory') and world.inventory.visible:
            if world.inventory.handle_event(e):
                continue
        if e.type == SDL_KEYDOWN and e.key == SDLK_e:
            world.inventory.toggle()
            return

        if e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
            game_framework.change_mode(GAME_PROJECT)
        else:
            world.player.handle_event(e)

def update():
    frame_time = 0.04
    world.update(frame_time)
    world.handle_collision()
    world.handle_attack_collision()
    world.player.late_update()
    if hasattr(world, "crops"):
        for crop in world.crops:
            crop.update(frame_time)
    if hasattr(world, 'ui'):
        world.ui.update(game_framework.frame_time)

    # if len(world.monsters) == 0 and not hasattr(world, "spawned_portal"):
    if not hasattr(world, "spawned_portal"):
        portal = DungeonPortal()
        world.add_object(portal, 0)
        world.add_collision_pair('player:portal', world.player, portal)

        world.spawned_portal = True
    delay(frame_time)

def draw():
    clear_canvas()
    background.draw(640, 360)
    world.render()
    if hasattr(world, 'inventory'):
        world.inventory.draw()

    if hasattr(world, 'ui'):
        world.ui.draw_hp(world.player.hp)
        world.ui.draw_gold(world.gold)

    update_canvas()

def pause():
    pass

def resume():
    pass
