from pico2d import *
import game_framework
import dungeon_mode,world, GAME_PROJECT
next_stage = 1
loading = 1.0

load_timer = 0.0

def start(target_stage: int = 1):

    global next_stage, loading
    next_stage = target_stage

def init():
    global load_timer,image
    image = load_image('Enter_dungeon_framework.png')
    load_timer = 0.0
    pass

def finish():
    pass

def update():
    global load_timer, loading
    load_timer += game_framework.frame_time

    if load_timer >= loading:
        try:
            dungeon_mode.init(stage=next_stage)
        except TypeError:
            dungeon_mode.init()
        game_framework.change_mode(dungeon_mode)

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
            game_framework.change_mode(GAME_PROJECT)
        else:
            world.player.handle_event(e)

def draw():
    clear_canvas()
    image.draw(640,360)
    update_canvas()

def pause():  pass
def resume(): pass


