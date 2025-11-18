from pico2d import *

class Inventory:
    def __init__(self):
        self.image = load_image('inventory.png')
        self.visible = False
        self.x, self.y = 640, 360
        self.w, self.h = 800, 512
        self.inv_h = 400
        self.quickslot_h = 112

    def toggle(self):
        self.visible = not self.visible
        print("Inventory Visible:", self.visible)

    def draw(self):
        if self.visible:
            self.image.clip_draw(0, 112, self.w, self.inv_h,self.x,self.y,self.w,self.inv_h)

        self.image.clip_draw(0,0,self.w,self.quickslot_h,self.x,self.y - 310, self.w*0.9, self.quickslot_h*0.9)

    def handle_event(self, event):
        if not self.visible:
            return False

        if event.type == SDL_KEYDOWN and event.key in (SDLK_ESCAPE, SDLK_e):
            self.toggle()
            return True
        return False
