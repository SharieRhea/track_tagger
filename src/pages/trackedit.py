from flet import (
    Column, 
    Container, 
    SafeArea, 
)

from controls.sidebar import Sidebar
from util.state import State

class TrackEditPage(Container):
    def __init__(self, state: State):
        super().__init__()
        self.state = state

        sidebar = Sidebar(state)

        # put all the content together on the page
        self.content = SafeArea(content=Column(controls=[
            sidebar.content
        ]))
