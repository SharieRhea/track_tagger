from typing import List
from flet import Page, WindowResizeEvent
from flet.core.file_picker import FilePickerFile

class State:
    def __init__(self, page: Page):
        self.page = page

        self.files: List[FilePickerFile] = []

        self.use_lastfm: bool = True
        self.lastfm_key: str | None = self.page.client_storage.get("lastfm_key")
        self.auto_accept_tags = self.page.client_storage.get("auto_accept_tags")

        self.current_file_index = 0

        self.height = self.page.window.height
        # for some reason the height is always too big, at least on linux
        if self.height is not None:
            self.height = self.height - 30
        self.width = self.page.window.width

    def on_resized(self, event: WindowResizeEvent):
        # reset the dimensions
        # for some reason the height is always too big, at least on linux
        self.height = event.height - 30
        self.width = event.width
        # force a page update so anything using the height and width readjusts
        self.page.update()
