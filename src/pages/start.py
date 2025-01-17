import flet
from flet import (
    Column,
    Container,
    Page,
    Ref,
    Row,
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
        self.file_picker = FilePickerControl(self.page, file_number_ref)
        # make a row to hold the file picker button and number of files display
        files = Row(controls=[self.file_picker.picker_button, file_number])

        self.key_field = KeyFieldControl("last.fm API key", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        self.tag_chips = TagChipsControl(self.page)

        self.content = Column(controls=[
            Text("Welcome to track_tagger!", theme_style=flet.TextThemeStyle.TITLE_LARGE),
            files,
            self.key_field.field,
            self.tag_chips.content
        ])
