from typing import List
from flet import Page
from flet.core.file_picker import FilePickerFile

class State:
    def __init__(self, page: Page):
        self.page = page

        self.files: List[FilePickerFile] = []

        self.use_lastfm: bool = True
        self.lastfm_key: str | None = self.page.client_storage.get("lastfm_key")
        self.auto_accept_tags = self.page.client_storage.get("auto_accept_tags")

        self.current_file_index = 0
