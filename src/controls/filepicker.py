from flet import (
    FilePickerFileType,
    OutlinedButton,
    FilePicker,
    FilePickerResultEvent,
    Ref,
    Text,
)

from util.state import State

# TODO: music tag can handle other audio types like wav, update text to be agnostic towards audio file type

class FilePickerControl():
    def __init__(self, state: State, file_number_reference: Ref[Text]):
        self.state = state
        self.file_number_reference = file_number_reference
        self.picker = FilePicker(on_result=self.on_file_picker_result)

        # set the dialog to appear as an overlay so it does not shift existing page content
        self.state.page.overlay.append(self.picker)
        self.state.page.update()

        self.picker_button = OutlinedButton(
            "Choose .mp3 files...",
            on_click=lambda _: self.picker.pick_files(allow_multiple=True, file_type=FilePickerFileType.AUDIO)
        )

        # begin with no files
        self.files = []
        self.file_number_reference.current.value = f"{len(self.files)} files selected"

    def on_file_picker_result(self, event: FilePickerResultEvent):
        if event.files is None:
            self.files = []
        else:
            # ensure only .mp3 files are selected
            self.files = list(filter(lambda it: ".mp3" in it.name, event.files))
        # make sure the page gets updated to display the newly selected files
        self.file_number_reference.current.value = f"{len(self.files)} files selected"
        self.state.page.update()

    def save_info(self):
        self.state.files = self.files
