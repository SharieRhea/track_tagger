import flet
from flet import (
    Column,
    Container,
    Icon,
    Page,
    Ref,
    Row,
    SafeArea,
    Switch,
    Text,
    TextField,
    Tooltip,
)
from controls.filepicker import FilePickerControl
from controls.keyfield import KeyFieldControl
from controls.tagchips import TagChipsControl

class StartPage(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

        # create a reference for the file picker control so that updates make it back to the page
        # TODO: error check this, maybe just remove files that are not mp3s?
        file_number_ref = Ref[Text]()
        file_number = Text(ref=file_number_ref, value="")
        file_picker = FilePickerControl(self.page, file_number_ref)

        # make a row to hold the file picker button and number of files display
        files = Row(controls=[file_picker.picker_button, file_number])

        # allow for changing file names
        # TODO: error check this, must be a valid format
        filename_field = TextField(
            label="Filename Format",
            hint_text="%t - %a",
            suffix_text=".mp3",
            width = 500
        )
        filename_info = Icon(
            name=flet.Icons.INFO_OUTLINED, 
            tooltip=Tooltip("Use the following specifiers to create a custom filename scheme.\n"\
                "Leave this field blank if you do not want filenames to be changed.\n"\
                "  %t track title\n"\
                "  %a track artist\n"\
                "  %at album title\n"\
                "  %aa album artist"
            )
        )
        filename = Row(controls=[filename_field, filename_info])

        # toggle for whether or not to use last.fm
        self.lastfm = True
        lastfm_switch = Switch(label="Use last.fm to search for track info?", on_change=self.toggle_lastfm, value=True)

        # last.fm only fields
        key_field = KeyFieldControl("last.fm API Key", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        # TODO: make this link clickable, will probably need to use the markdown renderer
        key_info = Icon(name=flet.Icons.INFO_OUTLINED, tooltip=Tooltip("To obtain an API key visit: https://www.last.fm/api/account/create"))
        key_row = Row(controls=[key_field.field, key_info])
        tag_chips = TagChipsControl(self.page, "Tags to automatically accept:")
        self.lastfm_fields = Column(controls=[key_row, tag_chips.content])

        # put all the content together on the page
        self.content = SafeArea(content=Column(controls=[
            Text("Welcome to track_tagger!", theme_style=flet.TextThemeStyle.HEADLINE_LARGE),
            files,
            filename,
            lastfm_switch,
            self.lastfm_fields
        ]))

    def toggle_lastfm(self, _):
        self.lastfm_fields.visible = not self.lastfm_fields.visible
        if self.content is not None:
            self.content.update()
