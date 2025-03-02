import os
from flet import (
    AlertDialog,
    Column,
    Container,
    CrossAxisAlignment,
    FilePicker,
    FilePickerFileType,
    FilePickerResultEvent,
    FilledButton,
    FilledTonalButton,
    FloatingActionButton,
    Image,
    OutlinedButton,
    Ref,
    Row, 
    SafeArea,
    SnackBar,
    Stack,
    Text,
    TextButton,
    TextField,
    VerticalDivider,
)
from flet.app import flet

from controls.sidebar import Sidebar
from controls.tagchips import TagChipsControl
from util import metadata, query
from util.entrystatus import EntryStatus
from util.state import State

class TrackEditPage(Container):
    def __init__(self, state: State):
        super().__init__()
        self.state = state
        self.state.trackedit_page = self

        self.sidebar = Sidebar(state)

        self.page_title_ref = Ref[Text]()
        page_title = Text(ref=self.page_title_ref, value=self.state.files[self.state.current_index]["name"], theme_style=flet.TextThemeStyle.HEADLINE_LARGE)

        self.title_field = TextField(
            label="Title",
            width=500
        )
        self.artist_field = TextField(
            label="Artist",
            width=500
        )
        self.album_field = TextField(
            label="Album",
            width=500
        )
        self.album_artist_field = TextField(
            label="Album Artist",
            width=500
        )

        self.tags = TagChipsControl(self.state, "track_tags", "Tags")

        self.album_image = Image(gapless_playback=True, border_radius=10, height=400, width=400)

        left_column = Column(controls=[
            page_title,
            self.title_field,
            self.artist_field,
            self.album_field,
            self.album_artist_field,
            self.tags.content
        ], expand=2)

        buttons = Column(controls=[
            OutlinedButton("Search last.fm", disabled=not self.state.use_lastfm, on_click=self.on_click_search_lastfm),
            OutlinedButton("Save and Exit", icon=flet.Icons.EXIT_TO_APP_ROUNDED, on_click=lambda _: self.state.page.open(self.end_dialog)),
            FilledButton("Save and Continue", icon=flet.Icons.ARROW_FORWARD_ROUNDED, on_click=self.on_click_continue)
        ], horizontal_alignment=flet.CrossAxisAlignment.END)

        album_image_stack = Stack(controls=[
            self.album_image,
            Container(content=FloatingActionButton(
                icon=flet.Icons.EDIT_ROUNDED, 
                mini=True, 
                on_click=self.on_click_edit_album_image), 
            alignment=flet.alignment.bottom_right,
            margin=16)
        ], height=300, width=300)

        right_column = Column(controls=[
            album_image_stack,
            buttons
        ], alignment=flet.MainAxisAlignment.SPACE_BETWEEN, horizontal_alignment=CrossAxisAlignment.END, expand=1)

        self.end_dialog = AlertDialog(
            modal=True,
            title=Text("Do you wish to go back to the start page?"),
            content=Text("Only saved files will keep their modifications."),
            actions=[
                FilledTonalButton("Yes", on_click=self.back_to_start),
                TextButton("No", on_click=lambda _: self.state.page.close(self.end_dialog)),
            ],
        )

        # put all the content together on the page
        self.content = SafeArea(content=Row(controls=[
            self.sidebar.content,
            VerticalDivider(thickness=3),
            left_column,
            right_column
        ], expand=True,
        height=self.state.height, width=self.state.width))

        # try to read metadata for the first file
        self.read_metadata()

    def on_click_continue(self, _):
        data = (
            self.title_field.value,
            self.artist_field.value,
            self.album_field.value,
            self.album_artist_field.value,
            self.album_image,
            [tag for (tag, selected) in self.tags.tags if selected]
        )
        metadata.write_metadata(self.state.files[self.state.current_index]["path"], data)        

        # FIX: filename is not being updated in the sidebar and file cannot be found if trying to navigate back to it 
        if self.state.filename_format is not None and self.state.filename_format is not "":
            # FIX: this will probably break on windows because of the slash direction
            parent_directory = os.path.dirname(self.state.files[self.state.current_index]["path"]) + "/"
            new_filename = metadata.format_filename(self.state.filename_format, data[0], data[1], data[2], data[3])
            os.rename(
                self.state.files[self.state.current_index]["path"], 
                parent_directory + new_filename + ".mp3"
            )
            # update the path in the files list in case of future access
            self.state.files[self.state.current_index]["path"] = new_filename

        # set the current file to "saved" status
        self.state.files[self.state.current_index]["status"] = EntryStatus.SAVED
        
        self.state.current_index += 1
        # go back to start page if done, otherwise move to next file
        if self.state.current_index >= len(self.state.files):
            # in case the user does not exit
            self.state.current_index -= 1
            self.state.page.open(self.end_dialog)
        else:
            self.read_metadata()
            self.sidebar.initialize_items()
            self.state.page.update()

    def read_metadata(self):
        data = metadata.read_metadata(self.state.files[self.state.current_index]["path"])

        # set the current file to "read" status if not already
        if self.state.files[self.state.current_index]["status"] == EntryStatus.UNREAD:
            self.state.files[self.state.current_index]["status"] = EntryStatus.READ
        self.sidebar.initialize_items()

        self.page_title_ref.current.value = self.state.files[self.state.current_index]["name"]
        self.title_field.value = data[0]
        self.artist_field.value = data[1]
        self.album_field.value = data[2]
        self.album_artist_field.value = data[3]
        if data[4] is not None:
            self.album_image.src_base64 = data[4]
        else:
            self.album_image.src = "generic_album_cover.jpg"
            self.album_image.src_base64 = None
        self.tags.update_tags(data[5])

    def on_click_search_lastfm(self, _):
        # search based on what's entered in title and artist fields
        title = self.title_field.value
        artist = self.artist_field.value

        # make sure required info is there
        if title is None or title == "":
            self.title_field.error_text="A title is required to search last.fm!"
            self.title_field.update()
            return
        self.title_field.error_text = None
        if artist is None or artist == "":
            self.artist_field.error_text="An artist is required to search last.fm!"
            self.artist_field.update()
            return
        self.artist_field.error_text = None

        info = query.track_getinfo(self.state.lastfm_key, title, artist)
        if info is None or "track" not in info:
            self.state.page.overlay.append(SnackBar(
                content=Text(f"Unable to find a match for {title} by {artist}!", color=flet.Colors.ON_ERROR_CONTAINER), 
                open=True, 
                bgcolor=flet.Colors.ERROR_CONTAINER
            ))
            self.state.page.update()
            return

        # update everything according to what was found from lastfm
        self.title_field.value = info["track"]["name"]
        self.artist_field.value = info["track"]["artist"]["name"]

        if "album" in info["track"]:
            self.album_field.value = info["track"]["album"]["title"]
            self.album_artist_field.value = info["track"]["album"]["artist"]

            # see if there is a valid album image cover
            # -1 to get the largest image resolution available
            album_image_url = info["track"]["album"]["image"][-1]["#text"]
            if album_image_url != "":
                self.album_image.src = album_image_url
                self.album_image.src_base64 = None

        # populate any tags
        tags_to_add = []
        for tag in info["track"]["toptags"]["tag"]:
            tags_to_add.append(tag["name"])
        self.tags.update_tags(tags_to_add, lastfm=True)

        # update the page to show all changes
        if self.content is not None:
            self.content.update()

    def on_click_edit_album_image(self, _):
        picker = FilePicker(on_result=self.on_album_image_result)
        # set the dialog to appear as an overlay so it does not shift existing page content
        self.state.page.overlay.append(picker)
        self.state.page.update()
        picker.pick_files(allow_multiple=False, file_type=FilePickerFileType.IMAGE)

    def on_album_image_result(self, event: FilePickerResultEvent):
        if event.files is not None:
            self.album_image.src_base64 = None
            self.album_image.src = event.files[0].path
            self.album_image.update()

    def back_to_start(self, _):
        self.state.page.close(self.end_dialog)
        self.state.page.go("/start")
