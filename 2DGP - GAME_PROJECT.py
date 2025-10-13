from pico2d import *
import random

class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(640, 360)

class Player:
    def __init__(self):
        self.image = load_image('_idle.png')
        self.x,self.y = 80,120
        self.frame = 0
        self.w = 120
        self.h = 80

    def update(self):
        self.frame = (self.frame + 1) % 10

    def draw(self):
        self.image.clip_draw(self.frame * self.w, 0, self.w, self.h, self.x, self.y,self.w*3,self.h*3)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
            
            
open_canvas(1280, 720)


def reset_world():
    global running, background,player
    running = True
    background = Background()
    player = Player()
    pass


reset_world()


def update_world():
    #background.update()
    player.update()
    pass


def render_world():
    clear_canvas()
    background.draw()
    player.draw()
    update_canvas()
    pass


while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)



close_canvas()

