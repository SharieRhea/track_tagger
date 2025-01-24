from flet import (
    ListView, 
    Text,
)

from util.state import State

class Sidebar():
    def __init__(self, state: State):
        self.state = state
        self.items = []
        self.initialize_items()

        self.content = ListView(controls=self.items)

    def initialize_items(self):
        for file in self.state.files:
            self.items.append(Text(file.name))
