from flet import (
    Column,
    Container,
    CrossAxisAlignment,
    FilePicker,
    FilePickerFileType,
    FilePickerResultEvent,
    FilledButton,
    FloatingActionButton,
    Image,
    OutlinedButton,
    Ref,
    Row, 
    SafeArea,
    SnackBar,
    Stack,
    Text,
    TextField,
    VerticalDivider,
)
from flet.app import flet

from controls.sidebar import Sidebar
from controls.tagchips import TagChipsControl
from util import metadata, query
from util.state import State

class TrackEditPage(Container):
    def __init__(self, state: State):
        super().__init__()
        self.state = state
        self.state.set_trackedit_page(self)

        self.sidebar = Sidebar(state)

        self.page_title_ref = Ref[Text]()
        page_title = Text(ref=self.page_title_ref, value=self.state.files[self.state.current_file_index].name, theme_style=flet.TextThemeStyle.HEADLINE_LARGE)

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

        self.album_image = Image(src="generic_album_cover.jpg", gapless_playback=True, border_radius=10, height=400, width=400)

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
            FilledButton("Continue", icon=flet.Icons.ARROW_FORWARD_ROUNDED, on_click=self.on_click_continue)
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
            self.tags.tags
        )
        metadata.write_metadata(self.state.files[self.state.current_file_index].path, data)        
        self.state.current_file_index += 1
        # go back to start page if done, otherwise move to next file
        if self.state.current_file_index >= len(self.state.files):
            # self.state.page.controls = [StartPage(self.state)]
            self.state.page.update()
        else:
            self.read_metadata()
            self.sidebar.initialize_items()
            self.state.page.update()

    def read_metadata(self):
        data = metadata.read_metadata(self.state.files[self.state.current_file_index].path)
        self.page_title_ref.current.value = self.state.files[self.state.current_file_index].name
        self.title_field.value = data[0]
        self.artist_field.value = data[1]
        self.album_field.value = data[2]
        self.album_artist_field.value = data[3]
        self.album_image.src_base64 = data[4]
        if self.album_image.src_base64 is not None:
            self.album_image.src = None
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
        self.tags.update_tags(tags_to_add)

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
