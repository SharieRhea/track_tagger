from flet import (
    Container,
    ListView, 
    Text,
)
import flet

from util.state import State

class Sidebar():
    def __init__(self, state: State):
        self.state = state
        self.items = []
        self.initialize_items()

        self.content = ListView(
            controls=self.items,
            width=250
        )

    def initialize_items(self):
        for index in range(0, len(self.state.files)):
            bgcolor = flet.Colors.SURFACE_CONTAINER_HIGHEST
            # make it obvious which song is being edited currently
            if index == self.state.current_file_index:
                bgcolor = flet.Colors.SECONDARY_CONTAINER
            self.items.append(Container(
                content=Text(self.state.files[index].name), 
                border_radius=flet.border_radius.all(50), 
                bgcolor=bgcolor, 
                ink=True,
                margin=flet.margin.symmetric(4, 0), 
                padding=flet.padding.symmetric(4, 12),
                # FIX: this always uses the last index, find a way to not use only one reference for this?
                on_click=lambda _: self.on_click(index)
            ))

    def on_click(self, index):
        self.state.current_file_index = index
