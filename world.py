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
        for o in layer[:]:
            try:
                o.update(frame_time)
            except TypeError:
                o.update()
            if hasattr(o, "is_dead") and o.is_dead():
                layer.remove(o)

def render(): #그리는 기능
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o, layer=None):
    for layer in world:
        if o in layer:
            layer.remove(o)
            break

    for group, (A, B) in list(collision_pairs.items()):
        if o in A:
            A.remove(o)
        if o in B:
            B.remove(o)

def clear():
    global gametime
    saved_gametime = gametime
    for layer in world:
        layer.clear()
    gametime = saved_gametime
    collision_pairs.clear()
    
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

def handle_collision():
    for group, (A, B) in collision_pairs.items():
        for a in A:
            for b in B:
                if collide(a, b):
                    if hasattr(a, 'handle_collision'):
                        a.handle_collision(group, b)
                    if hasattr(b, 'handle_collision'):
                        b.handle_collision(group, a)

def handle_attack_collision():
    global player

    if player is None:
        return

    atk_bb = player.get_attack_bb()
    if atk_bb is None:
        return

    l1, b1, r1, t1 = atk_bb

    for obj in world[1]:
        if not hasattr(obj, 'get_bb'):
            continue

        l2, b2, r2, t2 = obj.get_bb()

        if (l1 > r2) or (r1 < l2) or (t1 < b2) or (b1 > t2):
            continue

        obj.handle_collision('player:attack', player)
