from pico2d import *
from crop import Crop
import world
from text_ani import TextAni

TILE_SIZE = 32

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN
def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

class Plant:
    def __init__(self,player):
        self.player = player
        self.image_right = load_image('harvest.png')
        self.image_left = load_image('harvest_R.png')
        self.image = self.image_right
        self.frame = 0

    def enter(self, event):
        inv = world.inventory
        slot_index = inv.selected_quickslot
        inv_index = inv.quickslots[slot_index]

        self.frame = 0
        self.image = self.image_right if self.player.dir == 1 else self.image_left

        if inv_index is None:
            print("퀵슬롯이 비어있습니다.")
            return

        item = inv.items[inv_index]

        if not item["id"].startswith("seed_"):
            print("작물은 심을 수 없습니다. 씨앗만 심을 수 있습니다.")
            return

        if item["id"].startswith("seed_"):
            crop_type = item["id"][5:]
        else:
            crop_type = item["id"]


        tile_x = int(self.player.x // TILE_SIZE)
        tile_y = int(120 // TILE_SIZE)

        if not world.ground.can_plant(tile_x, tile_y):
            return

        for c in world.crops:
            cx = int(c.x // TILE_SIZE)
            cy = int(c.y // TILE_SIZE)
            if cx == tile_x and cy == tile_y:
                return

        new_crop = Crop(tile_x * TILE_SIZE + TILE_SIZE // 2, tile_y * TILE_SIZE + TILE_SIZE // 2, crop_type = crop_type)
        world.add_object(new_crop,1)
        world.crops.append(new_crop)

        item['count'] -= 1
        if item['count'] <= 0:
            #inv.items.pop(inv_index)

            for slot in inv.slots:
                if slot['item'] == inv_index:
                    slot['item'] = None

            for i in range(inv.quickslot_count):
                if inv.quickslots[i] == inv_index:
                    inv.quickslots[i] = None


    def exit(self,event):
        pass

    def do(self):
        if self.frame < 2:
            self.frame += 1
        else:
            self.frame = 2

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h, self.player.x, self.player.y, self.player.w * 3,self.player.h * 3)


class Harvest:
    def __init__(self, player):
        self.player = player
        self.image_right = load_image('harvest.png')
        self.image_left = load_image('harvest_R.png')
        self.image = self.image_right
        self.frame = 0

    def enter(self, event):
        self.frame = 0
        self.image = self.image_right if self.player.dir == 1 else self.image_left

        tile_x = int(self.player.x // TILE_SIZE)
        tile_y = int(120 // TILE_SIZE)

        existing_crop = None
        for c in world.crops:
            cx = int(c.x // TILE_SIZE)
            cy = int(c.y // TILE_SIZE)
            if cx == tile_x and cy == tile_y:
                existing_crop = c
                break
        if existing_crop is None:
            return

        if existing_crop and existing_crop.stage <= existing_crop.max_stage:
            existing_crop.harvest()

            crop_type = existing_crop.crop_type
            world.inventory.add_item(crop_type)

            name_kr = {
                "corn": "옥수수",
                "pumpkin": "호박",
                "potato": "감자",
                "strawberry": "딸기"
            }

            world.add_object(TextAni(self.player.x, self.player.y + 40, f"{name_kr[crop_type]} +1",duration = 1.0),3)
            world.crops.remove(existing_crop)


    def exit(self, event):
        pass

    def do(self):
        if self.frame < 2:
            self.frame += 1
        else:
            self.frame = 2

    def draw(self):
        self.image.clip_draw(self.frame * self.player.w, 0, self.player.w, self.player.h,
                             self.player.x, self.player.y, self.player.w * 3, self.player.h * 3)