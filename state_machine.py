class StateMachine:
    def __init__(self,start_state,rules,char):
        self.char = char
        self.current_state = start_state
        self.rules = rules
        self.current_state.enter(('START',0))
        pass

    def update(self):
        self.current_state.do()
        pass

    def draw(self):
        self.current_state.draw()
        pass

    def handle_state_event(self,state_event):
        for check_event,next_state in self.rules[self.current_state].items():
            if check_event(state_event):
                self.next_state = self.rules[self.current_state][check_event]
                self.next_state.prev_state = self.current_state
                self.current_state.exit(state_event)
                self.current_state = self.next_state
                self.next_state.enter(state_event)
                return
        pass

    def change_state(self,next_state):
        self.current_state.exit(('CHANGE',0))
        self.current_state = next_state
        self.current_state.enter(('CHANGE',0))
