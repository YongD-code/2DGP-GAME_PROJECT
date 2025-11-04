ground_y = 228

# layer 0 = 배경
# layer 1 = 건물, 지형
# layer 2 = 캐릭터, NPC, 포탈
# layer 3 = UI
world = [[],[],[],[]]
crops = []

player = None
background = None
ground = None
blacksmith = None
house = None
portal = None
npc = None
gametime = None

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
    for layer in world:
        layer.clear()

def set_ground_y(y):
    global ground_y
    ground_y = y
