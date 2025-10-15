class StateMachine:
    def __init__(self,start_state,char):
        self.current_state = start_state
        self.current_state.enter(self.char)
        self.char = char
        pass

    def update(self):
        self.current_state.update(self.char)
        pass

    def draw(self):
        self.current_state.draw(self.char)
        pass