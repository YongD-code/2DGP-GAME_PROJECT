from pico2d import *
import game_framework
import title_mode

image = None
logo_start_time = 0.0

def init():
    global image,logo_start_time
    image = load_image('tuk_credit.png')
    logo_start_time = get_time()
    pass

def finish():
    global image
    del image
    pass

def update():
    if get_time() - logo_start_time >= 2.0:
        game_framework.change_mode(title_mode)
    pass

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass

def handle_events():
    event_list = get_events() #버퍼로부터 모든 입력을 갖고 온다. 일단.
    #no nothing
    pass



def pause():
    pass

def resume():
    pass
