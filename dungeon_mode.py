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


stage_num = 1
def init(stage = 3):
    global background, player,dungeon_map, stage_num
    if stage is not None:
        stage_num = stage
    background = load_image('dungeon_bg.png')
    print(f"=== ENTERING DUNGEON STAGE {stage_num} ===")
    world.clear()

    player = Player()
    player.x, player.y = 110,180
    world.player = player
    world.set_ground_y(180)
    world.set_boundary(110, 1170)
    world.add_object(player, 2)
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

        for t in world.dungeon_map.get_tiles():
            world.add_collision_pair('player:tile', world.player, t)

        for s in slime_list:
            world.add_collision_pair('player:slime', world.player, s)

        portal = DungeonPortal()
        world.add_object(portal, 0)
        world.add_collision_pair('player:portal', player, portal)

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


        for t in world.dungeon_map.get_tiles():
            world.add_collision_pair('player:tile', world.player, t)

        for s in skeleton_list:
            world.add_collision_pair('player:skeleton', world.player, s)

        portal = DungeonPortal()
        world.add_object(portal, 0)
        world.add_collision_pair('player:portal', player, portal)

    elif stage_num == 3:
        dungeon_map = DungeonMap(stage_num)
        world.dungeon_map = dungeon_map
        world.add_object(dungeon_map,0)


        for t in world.dungeon_map.get_tiles():
            world.add_collision_pair('player:tile', world.player, t)


        portal = DungeonPortal()
        world.add_object(portal, 0)
        world.add_collision_pair('player:portal', player, portal)

def finish():
    world.clear()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
            game_framework.change_mode(GAME_PROJECT)
        else:
            world.player.handle_event(e)

def update():
    frame_time = 0.04
    world.update(frame_time)
    world.handle_collision()
    world.player.late_update()
    delay(frame_time)

def draw():
    clear_canvas()
    background.draw(640, 360)
    world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
