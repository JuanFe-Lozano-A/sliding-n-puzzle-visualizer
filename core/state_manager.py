from enum import Enum

class GameState(Enum):
    PLAYING = 1
    SOLVING = 2
    PAUSED = 3

class StateManager:
    def __init__(self):
        self.state = GameState.PLAYING

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
