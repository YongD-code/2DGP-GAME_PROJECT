from pico2d import *


class Inventory:
    def __init__(self):
        self.image = load_image('inventory.png')
        self.heal_img = load_image("heal_Potion.png")
        self.attack_img = load_image("attack_Potion.png")

        self.potion_images = {
            "potion_heal": self.heal_img,
            "potion_attack": self.attack_img,
        }
        self.visible = False
        self.x, self.y = 640, 360
        self.w, self.h = 800, 512
        self.inv_h = 400
        self.quickslot_h = 112
        self.quickslot_offset_y = -310
        self.quickslot_R_offset_x = 225
        self.quickslot_R_offset_y = 10
        self.cols = 6
        self.rows = 5
        self.slot_size = 54
        self.padding = 6
        self.slots = []
        self.items = []
        self.dragging = False
        self.drag_item_index = None
        self.drag_slot_index = None
        self.drag_mouse_x = 0
        self.drag_mouse_y = 0
        self.quickslot_scale = 1.0
        self.quickslot_ui_scale = 1.0

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

        qy = self.y + self.quickslot_offset_y- self.quickslot_R_offset_y
        start_x = self.x - self.quickslot_R_offset_x
        self.gap = 54

        self.quickslot_positions = [
            (start_x + i * self.gap, qy) for i in range(self.quickslot_count)
        ]

        self.item_icons = {
            "corn": {"col": 0, "row": 11},
            "pumpkin": {"col": 0, "row": 10},
            "potato": {"col": 0, "row": 9},
            "strawberry": {"col": 0, "row": 8},

            "seed_corn": {"col": 5, "row": 11},
            "seed_pumpkin": {"col": 5, "row": 10},
            "seed_potato": {"col": 5, "row": 9},
            "seed_strawberry": {"col": 5, "row": 8},
        }

        self.hover_item_index = None
        self.hover_slot_index = None
        self.tooltip_font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 18)

        self.item_descriptions = {
            "corn": "옥수수",
            "pumpkin": "호박",
            "potato": "감자",
            "strawberry": "딸기",

            "seed_corn": "옥수수 씨앗",
            "seed_pumpkin": "호박 씨앗",
            "seed_potato": "감자 씨앗",
            "seed_strawberry": "딸기 씨앗",

            "potion_heal": "체력 회복 물약",
            "potion_attack": "공격력 증가 물약"
        }

    def toggle(self):
        self.visible = not self.visible
        print("Inventory Visible:", self.visible)

    def combine_items(self, item_id1, item_id2):
        from text_ani import TextAni
        import world

        recipe = {
            ("corn", "pumpkin"): "potion_heal",
            ("pumpkin", "corn"): "potion_heal",

            ("strawberry", "potato"): "potion_attack",
            ("potato", "strawberry"): "potion_attack",
        }

        key = (item_id1, item_id2)
        if key not in recipe:
            return None

        result_item = recipe[key]

        def remove_one(target_id):
            for it in self.items:
                if it and it["id"] == target_id and it["count"] > 0:
                    it["count"] -= 1
                    return True
            return False

        if not remove_one(item_id1) or not remove_one(item_id2):
            return None

        self.add_item(result_item)

        return result_item


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

                slot_index = slot['item']
                if slot_index is not None:
                    item = self.items[slot_index]

                    base_size = 48
                    icon_size = int(base_size * self.quickslot_scale)

                    if item['id'] in self.potion_images:
                        img = self.potion_images[item['id']]
                        img.draw(x, y, icon_size, icon_size)
                    else:
                        icon = self.item_icons[item['id']]
                        self.draw_crop_icon(x, y, icon["col"], icon["row"], size=icon_size)

                    if item['count'] > 1:
                        self.draw_count_text(x, y, item['count'])
        ui_s = self.quickslot_ui_scale
        self.image.clip_draw( 0, 0, self.w, self.quickslot_h,self.x, self.y + self.quickslot_offset_y,
        self.w * 0.9 * ui_s, self.quickslot_h * 0.9 * ui_s)

        for i in range(self.quickslot_count):
            x, y = self.quickslot_positions[i]

            s = self.quickslot_scale
            draw_rectangle(x - 25 * s, y - 25 * s, x + 25 * s, y + 25 * s)

            if i == self.selected_quickslot:
                s = self.quickslot_scale
                draw_rectangle(x - 30* s, y - 30* s, x + 30* s, y + 30* s)

            slot_item_index = self.quickslots[i]

            if slot_item_index is not None:
                item = self.items[slot_item_index]

                base_size = 48
                icon_size = int(base_size * self.quickslot_scale)

                if item['id'] in self.potion_images:
                    img = self.potion_images[item['id']]
                    img.draw(x, y, icon_size, icon_size)
                else:
                    icon = self.item_icons[item['id']]
                    self.draw_crop_icon(x, y, icon["col"], icon["row"], size=icon_size)

                if item["count"] > 1:
                    self.draw_count_text(x, y, item["count"])

        if self.dragging and self.drag_item_index is not None:
            item = self.items[self.drag_item_index]
            mx, my = self.drag_mouse_x, self.drag_mouse_y

            base_size = 48
            icon_size = int(base_size * self.quickslot_scale)

            if item['id'] in self.potion_images:
                img = self.potion_images[item['id']]
                img.draw(mx, my, icon_size, icon_size)

            else:
                icon = self.item_icons[item['id']]
                self.draw_crop_icon(mx, my, icon["col"], icon["row"], size=icon_size)

        if self.visible and not self.dragging:
            self.draw_tooltip()

    def draw_count_text(self, x, y, count):
        if not hasattr(self, 'count_font'):
            self.count_font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 20)
        self.count_font.draw(x + 12, y - 20, f"{count}", (255,255,255))

    def draw_crop_icon(self, x, y, col, row, size=None):
        sx = col * self.crop_w
        sy = (self.crop_rows - 1 - row) * self.crop_h

        if size is None:
            size = int(48 * self.quickslot_scale)

        self.crop_sheet.clip_draw(sx, sy, self.crop_w, self.crop_h, x, y, size, size)


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
                if x - self.slot_size / 2 < mx < x + self.slot_size / 2 and \
                        y - self.slot_size / 2 < my < y + self.slot_size / 2:

                    if slot['item'] is not None:
                        self.dragging = True
                        self.drag_item_index = slot['item']
                        self.drag_slot_index = i
                        self.drag_mouse_x = mx
                        self.drag_mouse_y = my
                        return True

        if event.type == SDL_MOUSEMOTION:
            if self.dragging:
                self.drag_mouse_x = event.x
                self.drag_mouse_y = 720 - event.y
                return True

        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx, my = event.x, 720 - event.y
            for i, slot in enumerate(self.slots):
                x, y = slot['x'], slot['y']
                if x - self.slot_size / 2 < mx < x + self.slot_size / 2 and \
                        y - self.slot_size / 2 < my < y + self.slot_size / 2:
                    self.selected_slot = i
                    print(f"Selected slot {i}")
                    return True
            return False

        if event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
            if self.dragging:
                mx, my = event.x, 720 - event.y

                target_slot = None
                for i, slot in enumerate(self.slots):
                    x, y = slot['x'], slot['y']
                    if x - self.slot_size / 2 < mx < x + self.slot_size / 2 and \
                            y - self.slot_size / 2 < my < y + self.slot_size / 2:
                        target_slot = i
                        break

                origin_slot = self.drag_slot_index
                origin_item_index = self.drag_item_index

                self.dragging = False
                self.drag_item_index = None
                self.drag_slot_index = None

                if target_slot is None:
                    return True

                target_item_index = self.slots[target_slot]['item']

                if target_item_index is None:
                    self.slots[target_slot]['item'] = origin_item_index
                    self.slots[origin_slot]['item'] = None
                    return True

                item1 = self.items[origin_item_index]
                item2 = self.items[target_item_index]

                result = self.combine_items(item1["id"], item2["id"])

                if result is not None:
                    if item1["count"] <= 0:
                        self.slots[origin_slot]['item'] = None
                    if item2["count"] <= 0:
                        self.slots[target_slot]['item'] = None
                    return True

                self.slots[target_slot]['item'], self.slots[origin_slot]['item'] = \
                    self.slots[origin_slot]['item'], self.slots[target_slot]['item']

                return True
        if event.type == SDL_MOUSEMOTION:
            mx, my = event.x, 720 - event.y

            if not self.dragging:
                self.hover_item_index = None
                self.hover_slot_index = None

                for i, slot in enumerate(self.slots):
                    x, y = slot['x'], slot['y']
                    if x - self.slot_size / 2 < mx < x + self.slot_size / 2 and \
                            y - self.slot_size / 2 < my < y + self.slot_size / 2:

                        if slot['item'] is not None:
                            self.hover_item_index = slot['item']
                            self.hover_slot_index = i
                        break

        return False

    def add_item(self, item_id):
        for idx, it in enumerate(self.items):
            if it['id'] == item_id:
                it['count'] += 1
                return idx

        self.items.append({'id': item_id, 'count': 1})
        new_index = len(self.items) - 1

        for slot in self.slots:
            if slot['item'] is None:
                slot['item'] = new_index
                break

        return new_index

    def move_to_quickslot(self, slot_index):

        slot_item_index = self.slots[slot_index]['item']
        if slot_item_index is None:
            return

        for i in range(self.quickslot_count):
            if self.quickslots[i] is None:
                self.quickslots[i] = slot_item_index

                self.slots[slot_index]['item'] = None
                return

    def draw_tooltip(self):
        if self.hover_item_index is None or self.hover_slot_index is None:
            return

        slot = self.slots[self.hover_slot_index]
        sx, sy = slot['x'], slot['y']

        item = self.items[self.hover_item_index]
        item_id = item['id']
        desc = self.item_descriptions.get(item_id, "설명 없음")

        tx = sx - 40
        ty = sy + 40

        self.tooltip_font.draw(tx, ty, desc, (255, 255, 255))

    def update_quickslot_positions(self):
        qy = self.y + self.quickslot_offset_y - self.quickslot_R_offset_y
        start_x = self.x - self.quickslot_R_offset_x
        self.quickslot_positions = [
            (start_x + i * self.gap, qy) for i in range(self.quickslot_count)
        ]