import flet
from flet import (
    Chip,
    Column,
    IconButton,
    Ref,
    Row,
    Text,
    TextField
)

from util.state import State

class TagChipsControl():
    def __init__(self, state: State, key: str, header_text: str):
        self.state = state
        self.key = key
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
            Row([new_tag_field, new_tag_add_button])
        ])
        
        # either load tags from client storage or start with none
        stored_tags = self.state.page.client_storage.get(key)
        if stored_tags is None:
            self.tags = []
        else:
            self.tags = [(tag, True) for tag in stored_tags]
            for (tag, selected) in self.tags:
                self.chips_row_ref.current.controls.append(Chip(label=Text(tag), selected=selected, on_select=self.on_select, on_delete=self.on_delete))

    # TODO: these methods could be cleaned up and organized better

    def update_chips(self):
        # reset all chips
        self.chips_row_ref.current.controls = []
        # add a chip back in for each tag
        for (tag, selected) in self.tags:
            self.chips_row_ref.current.controls.append(Chip(label=Text(tag), selected=selected, on_select=self.on_select, on_delete=self.on_delete))
        self.content.update()

    def update_tags(self, tags, lastfm=False):
        self.tags = []
        self.chips_row_ref.current.controls = []
        for tag in tags:
            if tag != "":
                selected = True
                # if tags are coming from last.fm, only auto select if part of the auto accept group
                if lastfm:
                    selected = tag in self.state.auto_accept_tags
                self.tags.append((tag, selected))
                self.chips_row_ref.current.controls.append(Chip(label=Text(tag), selected=selected, on_select=self.on_select, on_delete=self.on_delete))

    def on_delete(self, event):
        self.tags.remove((event.control.label.value, event.control.selected))
        self.update_chips()

    def on_select(self, event):
        # find the element in the list for this tag and flip its selected value
        match = next(item for item in self.tags if item[0] is event.control.label.value)
        self.tags[self.tags.index(match)] = (match[0], not match[1])
        # NOTE: flet automatically changes the selected value for the actual chip control
        self.state.page.update()

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
        self.tags.append((self.new_tag_ref.current.value, True))
        self.new_tag_ref.current.value = ""
        self.update_chips()
        # set focus back on the field to enter another tag
        self.new_tag_ref.current.focus()

    def save_info(self):
        self.state.page.client_storage.set(self.key, [tag for (tag, _) in self.tags])
        if self.key == "auto_accept_tags":
            self.state.auto_accept_tags = self.state.page.client_storage.get("auto_accept_tags")
