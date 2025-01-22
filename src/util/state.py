from flet import Page

class State:
    def __init__(self, page: Page):
        self.page = page
        self.use_lastfm: bool = True
        self.lastfm_key: str | None = self.page.client_storage.get("lastfm_key")
        self.auto_accept_tags = self.page.client_storage.get("auto_accept_tags")
