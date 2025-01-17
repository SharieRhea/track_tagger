from flet import (
    TextField
)

class KeyFieldControl():
    def __init__(self, label: str, hint_text: str):
        self.field = TextField(
            label=label,
            hint_text=hint_text,
            password=True,
            can_reveal_password=True,
            width=500
        )
