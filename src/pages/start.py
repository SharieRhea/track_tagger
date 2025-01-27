import flet
from flet import (
    Column,
    Container,
    FilledButton,
    Icon,
    ListTile,
    Ref,
    Row,
    SafeArea,
    SnackBar,
    Switch,
    Text,
    TextField,
    Tooltip,
)

from controls.filepicker import FilePickerControl
from controls.keyfield import KeyFieldControl
from controls.tagchips import TagChipsControl
from pages.trackedit import TrackEditPage
from util.state import State

class StartPage(Container):
    def __init__(self, state: State):
        super().__init__()
        self.state = state

        # create a reference for the file picker control so that updates make it back to the page
        file_number_ref = Ref[Text]()
        file_number = Text(ref=file_number_ref, value="")
        self.file_picker = FilePickerControl(self.state, file_number_ref)

        # make a row to hold the file picker button and number of files display
        files = ListTile(leading=self.file_picker.picker_button, title=file_number)

        # allow for changing file names, use reference for error handling
        self.filename_field_ref = Ref[TextField]()
        filename_field = TextField(
            ref=self.filename_field_ref,
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
        self.key_field = KeyFieldControl(self.state, "lastfm_key", "last.fm API Key", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        # TODO: make this link clickable, will probably need to use the markdown renderer
        key_info = Icon(name=flet.Icons.INFO_OUTLINED, tooltip=Tooltip("To obtain an API key visit: https://www.last.fm/api/account/create"))
        key_row = Row(controls=[self.key_field.field, key_info])
        self.tag_chips = TagChipsControl(self.state, "auto_accept_tags", "Tags to automatically accept:")
        self.lastfm_fields = Column(controls=[key_row, self.tag_chips.content])

        # move on
        continue_button = FilledButton("Continue", icon=flet.Icons.ARROW_FORWARD_ROUNDED, on_click=self.on_click_continue)

        main_column = Column(controls=[
            Text("Welcome to track_tagger!", theme_style=flet.TextThemeStyle.HEADLINE_LARGE),
            files,
            filename,
            lastfm_switch,
            self.lastfm_fields,
        ], expand=8)

        button_column = Column(
            controls=[continue_button], 
            alignment=flet.MainAxisAlignment.END, 
            horizontal_alignment=flet.CrossAxisAlignment.END,
            expand=2
        )

        # put all the content together on the page
        self.content = SafeArea(content=Row(controls=[
            main_column,
            button_column
        ]), height=self.state.height, width=self.state.width)

    def toggle_lastfm(self, _):
        self.lastfm_fields.visible = not self.lastfm_fields.visible
        self.state.use_lastfm = self.lastfm_fields.visible
        if self.content is not None:
            self.content.update()

    def on_click_continue(self, _):
        # save to client_storage
        self.key_field.save_info()
        self.tag_chips.save_info()
        # save files to state
        self.file_picker.save_info()

        # error checking before we move on
        if len(self.state.files) == 0:
            self.state.page.overlay.append(SnackBar(
                content=Text("You must select at least one file to edit!", color=flet.Colors.ON_ERROR_CONTAINER), 
                open=True, 
                bgcolor=flet.Colors.ERROR_CONTAINER
            ))
            self.state.page.update()
            return

        if self.error_check_filename():
            return

        # if lastfm is being used, make sure the key works
        if self.state.use_lastfm and self.key_field.error_check():
            return

        # all good, move on to editing
        self.state.page.controls = [TrackEditPage(self.state)]
        self.state.page.update()
           
    def error_check_filename(self) -> bool:
        # if filename is blank, filenames will be left alone
        if self.filename_field_ref.current.value is None:
            return False

        illegal_characters = ["/", "<", ">", ":", "\"", "\\", "|", "?", "*"]
        for character in illegal_characters:
            if character in self.filename_field_ref.current.value:
                self.filename_field_ref.current.error_text = f"Invalid character '{character}' in format!"
                if self.content is not None:
                    self.content.update()
                return True

        # filename was valid, reset any error text for the field
        self.filename_field_ref.current.error_text = None
        if self.content is not None:
            self.content.update()
        return False
