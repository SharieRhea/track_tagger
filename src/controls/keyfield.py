from flet import TextField

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
