from typing import List
import flet
from flet import (
    Chip,
    Column,
    IconButton,
    Page,
    Row,
    Text,
    TextField
)

class TagChipsControl():
    def __init__(self, page: Page):
        self.page = page
        self.content = Column()
        self.tags = []
        self.chips = []
        self.new_tag_field = TextField(label="Tag Name", hint_text="pop rock", on_submit=self.on_click_add)
        self.new_tag_add_button = IconButton(icon=flet.Icons.ADD_ROUNDED, tooltip="add tag", on_click=self.on_click_add)
        self.content.controls = [
            Text("Auto-accept tags:"), 
            Row(self.chips),
            Row([self.new_tag_field, self.new_tag_add_button])
        ]

    def update_chips(self):
        self.chips = []
        for tag in self.tags:
            self.chips.append(Chip(label=Text(tag), on_delete=self.on_delete))
        self.content.controls[1] = Row(self.chips)
        self.content.update()
        self.page.update()

    def on_delete(self, event):
        self.tags.remove(event.control.label.value)
        self.update_chips()

    def on_click_add(self, _):
        if self.new_tag_field.value is not None and self.new_tag_field.value != "":
            self.tags.append(self.new_tag_field.value)
            self.new_tag_field.value = ""
            self.update_chips()
