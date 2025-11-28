from pico2d import *
import world

class DialogueUI:
    def __init__(self, npc_id, scripts):
        self.npc_id = npc_id
        self.scripts = scripts
        self.index = 0
        self.font = load_font('D2Coding-Ver1.3.2-20180524.ttf', 26)
        self.bg = load_image('dialogue_box.png')
        self.active = True

    def next(self):
        self.index += 1
        if self.index >= len(self.scripts):
            self.active = False
            return False
        return True

    def draw(self):
        self.bg.draw(640,120,600,100)

        text = self.scripts[self.index]
        self.font.draw(440, 120, text, (0, 0, 0))

