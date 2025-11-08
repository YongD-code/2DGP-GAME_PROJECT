from pico2d import *
import game_framework
import world
from player import Player
import GAME_PROJECT
from slime import Slime
from dungeon_tile import DungeonMap

def init():
    global background, player,dungeon_map
    background = load_image('dungeon_1stage.png')

    world.clear()

    dungeon_map = DungeonMap()
    world.dungeon_map = dungeon_map
    world.add_object(dungeon_map,0)

    player = Player()
    player.x, player.y = 110,180
    world.player = player
    world.set_ground_y(180)
    world.set_boundary(110, 1170)
    world.add_object(player, 1)
    if world.gametime is not None:
        world.add_object(world.gametime, 3)

    slime_list = [Slime(500, 85), Slime(900, 85)]
    for s in slime_list:
        world.add_object(s, 1)

    for t in world.dungeon_map.get_tiles():
        world.add_collision_pair('player:tile', world.player, t)
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
