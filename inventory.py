from pico2d import *


class Inventory:
    def __init__(self):
        self.image = load_image('inventory.png')
        self.visible = False
        self.x, self.y = 640, 360
        self.w, self.h = 800, 512
        self.inv_h = 400
        self.quickslot_h = 112
        self.quickslot_offset_y = -310
        self.cols = 6
        self.rows = 5
        self.slot_size = 54
        self.padding = 6
        self.slots = []
        self.items = []
        start_x = self.x - (self.cols * (self.slot_size + self.padding)) / 2 + self.slot_size / 2 + 32
        start_y = self.y + (self.rows * (self.slot_size + self.padding)) / 2 - self.slot_size / 2 - 32
        for row in range(self.rows):
            for col in range(self.cols):
                sx = start_x + col * (self.slot_size + self.padding)
                sy = start_y - row * (self.slot_size + self.padding)
                self.slots.append({'x': sx, 'y': sy, 'item': None})

        self.crop_sheet = load_image('crop.png')
        self.crop_cols = 10
        self.crop_rows = 12
        self.crop_w = 160 // self.crop_cols
        self.crop_h = 192 // self.crop_rows

        self.test_item = {'col': 0, 'row': 11}

        self.selected_slot = -1


    def toggle(self):
        self.visible = not self.visible
        print("Inventory Visible:", self.visible)

    def draw(self):
        if self.visible:
            self.image.clip_draw(
                0, self.quickslot_h, self.w, self.inv_h,
                self.x, self.y, self.w, self.inv_h
            )

            for i, slot in enumerate(self.slots):
                x, y = slot['x'], slot['y']
                draw_rectangle(x - self.slot_size / 2, y - self.slot_size / 2,
                               x + self.slot_size / 2, y + self.slot_size / 2)

                if i == self.selected_slot:
                    draw_rectangle(x - self.slot_size / 2 - 4, y - self.slot_size / 2 - 4,
                                   x + self.slot_size / 2 + 4, y + self.slot_size / 2 + 4)

                if i == 0:
                    self.draw_crop_icon(x, y, self.test_item['col'], self.test_item['row'])

        self.image.clip_draw(
            0, 0, self.w, self.quickslot_h,
            self.x, self.y + self.quickslot_offset_y,
                    self.w * 0.9, self.quickslot_h * 0.9
        )

    def draw_crop_icon(self, x, y, col, row):
        sx = col * self.crop_w
        sy = (self.crop_rows - 1 - row) * self.crop_h  # OpenGL 좌표계 보정
        self.crop_sheet.clip_draw(sx, sy, self.crop_w, self.crop_h, x, y, 48, 48)


    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key in (SDLK_ESCAPE, SDLK_e):
            self.toggle()
            return True

        if not self.visible:
            return False

        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx, my = event.x, 720 - event.y
            for i, slot in enumerate(self.slots):
                x, y = slot['x'], slot['y']
                if x - self.slot_size/2 < mx < x + self.slot_size/2 and \
                   y - self.slot_size/2 < my < y + self.slot_size/2:
                    self.selected_slot = i
                    print(f"Selected slot {i}")
                    return True
        return False

    def add_item(self, item_id):
        for it in self.items:
            if it['id'] == item_id:
                it['count'] += 1
                return

        self.items.append({'id': item_id, 'count': 1})
