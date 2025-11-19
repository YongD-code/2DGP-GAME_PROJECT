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

        self.quickslot_count = 10
        self.quickslots = [None] * self.quickslot_count

        self.selected_quickslot = 0
        self.quickslot_positions = []

        qy = self.y + self.quickslot_offset_y- 10
        start_x = self.x - 225
        gap = 54

        self.quickslot_positions = [
            (start_x + i * gap, qy) for i in range(self.quickslot_count)
        ]

        self.item_icons = {
            "corn": {"col": 0, "row": 11},
            "carrot": {"col": 1, "row": 11},
            "pumpkin": {"col": 2, "row": 11},
            "potato": {"col": 3, "row": 11}
        }
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

                if i < len(self.items):
                    item = self.items[i]

                    if item['id'] == 'corn':
                        self.draw_crop_icon(x, y, 0, 11)

                    if item['count'] > 1:
                        if not hasattr(self, 'count_font'):
                            self.count_font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 20)
                        self.count_font.draw(x + 10, y - 20, f"{item['count']}", (255, 255, 255))

        self.image.clip_draw(
            0, 0, self.w, self.quickslot_h,
            self.x, self.y + self.quickslot_offset_y,
                    self.w * 0.9, self.quickslot_h * 0.9)

        for i in range(self.quickslot_count):
            x, y = self.quickslot_positions[i]

            draw_rectangle(x - 25, y - 25, x + 25, y + 25)

            if i == self.selected_quickslot:
                draw_rectangle(x - 30, y - 30, x + 30, y + 30)

            slot_item_index = self.quickslots[i]

            if slot_item_index is not None:
                item = self.items[slot_item_index]

                icon = self.item_icons[item["id"]]
                self.draw_crop_icon(x, y, icon["col"], icon["row"])

                if item["count"] > 1:
                    self.draw_count_text(x, y, item["count"])


    def draw_count_text(self, x, y, count):
        if not hasattr(self, 'count_font'):
            self.count_font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 20)
        self.count_font.draw(x + 12, y - 20, f"{count}", (255,255,255))

    def draw_crop_icon(self, x, y, col, row):
        sx = col * self.crop_w
        sy = (self.crop_rows - 1 - row) * self.crop_h
        self.crop_sheet.clip_draw(sx, sy, self.crop_w, self.crop_h, x, y, 48, 48)


    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key in (SDLK_ESCAPE, SDLK_e):
            self.toggle()
            return True

        if not self.visible:
            return False
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            mx, my = event.x, 720 - event.y

            for i, slot in enumerate(self.slots):
                x, y = slot['x'], slot['y']
                if x - self.slot_size / 2 < mx < x + self.slot_size / 2 and \
                        y - self.slot_size / 2 < my < y + self.slot_size / 2:
                    self.move_to_quickslot(i)
                    return True

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

    def move_to_quickslot(self, slot_index):

        if slot_index >= len(self.items):
            return

        item = self.items[slot_index]

        target_slot = None
        for i in range(self.quickslot_count):
            if self.quickslots[i] is None:
                target_slot = i
                break

        if target_slot is None:
            print("퀵슬롯에 빈 칸이 없습니다.")
            return

        self.quickslots[target_slot] = slot_index

        # 인벤토리 item에서도 제거하고 싶으면 아래처럼:
        # (원하면 “인벤토리에도 남기기” 방식도 가능)
        self.items.pop(slot_index)
