from flet import TextField

from util import query
from util.state import State

class KeyFieldControl():
    def __init__(self, state: State, key: str, label: str, hint_text: str):
        self.state = state
        self.key = key

        self.field = TextField(
            label=label,
            hint_text=hint_text,
            value=self.state.lastfm_key,
            password=True,
            can_reveal_password=True,
            width=500
        )

    def save_info(self):
        # write the current key to client storage - persistent
        self.state.page.client_storage.set(self.key, self.field.value)
        # update state
        self.state.lastfm_key = self.field.value

    def error_check(self) -> bool:
        if self.field.value is None or self.field.value == "":
            self.field.error_text="Provide a last.fm key!"
            self.field.update()
            return True
        # check that the key is valid
        result = query.track_getinfo(self.state.lastfm_key, "Alley Cat", "All Under Heaven")
        if result is None:
            self.field.error_text="Invalid last.fm key!"
            self.field.update()
            return True
        # remove any error text that may be present
        self.field.error_text = None
        self.field.update()
        return False
