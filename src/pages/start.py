import flet
from flet import (
    Column,
    Container,
    Page,
    Ref,
    Row,
    Switch,
    Text,
)
from controls.filepicker import FilePickerControl
from controls.keyfield import KeyFieldControl
from controls.tagchips import TagChipsControl

class StartPage(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

        # create a reference for the file picker control so that updates make it back to the page
        file_number_ref = Ref[Text]()
        file_number = Text(ref=file_number_ref, value="")
        file_picker = FilePickerControl(self.page, file_number_ref)

        # make a row to hold the file picker button and number of files display
        files = Row(controls=[file_picker.picker_button, file_number])

        # toggle for whether or not to use last.fm
        self.lastfm = True
        lastfm_switch = Switch(label="Use last.fm", on_change=self.toggle_lastfm, value=True)

        key_field = KeyFieldControl("last.fm API key", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        tag_chips = TagChipsControl(self.page)
        self.lastfm_fields = Column(controls=[key_field.field, tag_chips.content])

        self.content = Column(controls=[
            Text("Welcome to track_tagger!", theme_style=flet.TextThemeStyle.TITLE_LARGE),
            files,
            lastfm_switch,
            self.lastfm_fields
        ])

    def toggle_lastfm(self, _):
        self.lastfm_fields.visible = not self.lastfm_fields.visible
        if self.content is not None:
            self.content.update()
