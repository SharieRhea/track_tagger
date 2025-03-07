from typing import Any, List
from flet import Page, WindowResizeEvent

class State:
    def __init__(self, page: Page):
        self.page = page
        self.trackedit_page: Any = None

        self.use_lastfm: bool = True
        self.lastfm_key: str | None = self.page.client_storage.get("lastfm_key")
        self.auto_accept_tags = self.page.client_storage.get("auto_accept_tags")

        self.filename_format: str | None = None

        self.files: List[dict[str, Any]] = []

        self.current_index = 0

        self.height = self.page.window.height
        # for some reason the height is always too big, at least on linux
        if self.height is not None:
            self.height = self.height - 30
        self.width = self.page.window.width

    def update_trackedit_page(self):
        if self.trackedit_page is not None:
            self.trackedit_page.read_metadata()
            self.page.update()

    def on_resized(self, event: WindowResizeEvent):
        # reset the dimensions
        # for some reason the height is always too big, at least on linux
        self.height = event.height - 30
        self.width = event.width
        # force a page update so anything using the height and width readjusts
        self.page.update()

    def clear(self):
        self.files.clear()
        self.trackedit_page = None
        self.use_lastfm = True
        self.lastfm_key = self.page.client_storage.get("lastfm_key")
        self.auto_accept_tags = self.page.client_storage.get("auto_accept_tags")
        self.current_index = 0
