import flet
from flet import (
    Chip,
    Column,
    CrossAxisAlignment,
    IconButton,
    Page,
    Ref,
    Row,
    Text,
    TextField
)

class TagChipsControl():
    def __init__(self, page: Page, header_text: str):
        self.page = page
        self.tags = []

        # make a reference so that error text can be added later if needed
        self.new_tag_ref = Ref[TextField]()
        new_tag_field = TextField(ref=self.new_tag_ref, label="Tag Name", hint_text="pop rock", on_submit=self.on_click_add, autofocus=True)
        new_tag_add_button = IconButton(icon=flet.Icons.ADD_ROUNDED, tooltip="add tag", on_click=self.on_click_add)

        # make a reference so chips can be modified later
        self.chips_row_ref = Ref[Row]()
        chips_row = Row(ref=self.chips_row_ref, controls=[], wrap=True)

        # add all the content
        self.content = Column([
            Text(header_text, theme_style=flet.TextThemeStyle.LABEL_LARGE), 
            chips_row,
            # alignment start prevents the add button from being moved down when error text appears on the field
            Row([new_tag_field, new_tag_add_button], vertical_alignment=CrossAxisAlignment.START)
        ])

    def update_chips(self):
        # reset all chips
        self.chips_row_ref.current.controls = []
        # add a chip back in for each tag
        for tag in self.tags:
            self.chips_row_ref.current.controls.append(Chip(label=Text(tag), on_delete=self.on_delete))
        self.content.update()

    def on_delete(self, event):
        self.tags.remove(event.control.label.value)
        self.update_chips()

    def on_click_add(self, _):
        # do not allow empty tags
        if self.new_tag_ref.current.value is None or self.new_tag_ref.current.value == "":
            self.new_tag_ref.current.error_text = "Tag Name cannot be empty!"
            self.content.update()
            # set focus back on the field to enter another tag
            self.new_tag_ref.current.focus()
            return
        # do not allow duplicate tags
        if self.new_tag_ref.current.value in self.tags:
            self.new_tag_ref.current.error_text = "You already have that tag!"
            self.content.update()
            # set focus back on the field to enter another tag
            self.new_tag_ref.current.focus()
            return

        # new tag is valid
        self.new_tag_ref.current.error_text = None
        self.tags.append(self.new_tag_ref.current.value)
        self.new_tag_ref.current.value = ""
        self.update_chips()
        # set focus back on the field to enter another tag
        self.new_tag_ref.current.focus()
