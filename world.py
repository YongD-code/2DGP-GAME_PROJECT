ground_y = 228
left_boundary = 30
right_boundary = 1250
# layer 0 = 배경
# layer 1 = 건물, 지형
# layer 2 = 캐릭터, NPC, 포탈
# layer 3 = UI
world = [[],[],[],[]]
crops = []
tiles = []

player = None
background = None
ground = None
blacksmith = None
house = None
portal = None
npc = None
gametime = None
dungeon_map = None

def add_object(o, layer):
    world[layer].append(o)

def update(frame_time): #업데이트하는 기능
    for layer in world:
        for o in layer:
            try:
                o.update(frame_time)
            except TypeError:
                o.update()

def render(): #그리는 기능
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o, layer):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

def clear():
    global gametime
    saved_gametime = gametime
    for layer in world:
        layer.clear()
    gametime = saved_gametime

def set_ground_y(y):
    global ground_y
    ground_y = y

def set_gametime(gt):
    global gametime
    gametime = gt

def set_boundary(left, right):
    global left_boundary, right_boundary
    left_boundary, right_boundary = left, right

def add_tiles(tile_list):
    global tiles
    tiles.extend(tile_list)

collision_pairs = {}

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()
    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False
    return True

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)