from flet import (
    Container,
    ListView,
    Ref, 
    Text,
)
import flet

from util.state import State

class Sidebar():
    def __init__(self, state: State):
        self.state = state

        self.reference = Ref[ListView]()
        self.content = ListView(
            ref=self.reference,
            width=250
        )
        self.initialize_items()

    def initialize_items(self):
        self.items = []
        for index in range(0, len(self.state.files)):
            bgcolor = flet.Colors.SURFACE_CONTAINER_HIGHEST
            # make it obvious which song is being edited currently
            if index == self.state.current_file_index:
                bgcolor = flet.Colors.SECONDARY_CONTAINER
            self.items.append(Container(
                content=Text(self.state.files[index].name), 
                border_radius=flet.border_radius.all(10), 
                bgcolor=bgcolor, 
                ink=True,
                margin=flet.margin.symmetric(4, 0), 
                padding=flet.padding.symmetric(4, 12),
                on_click=lambda _, index=index: self.on_click(index)
            ))
        self.reference.current.controls = self.items

    def on_click(self, index):
        self.state.current_file_index = index
        # reinitialize to update which one is highlighted
        self.initialize_items()
        # read the metadata for the new current file and update
        self.state.update_trackedit_page()
