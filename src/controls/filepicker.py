from flet import (
    OutlinedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Ref,
    Text,
)

class FilePickerControl():
    def __init__(self, page: Page, file_number_reference: Ref[Text]):
        self.page = page
        self.file_number_reference = file_number_reference
        self.picker = FilePicker(on_result=self.on_file_picker_result)
        # set the dialog to appear as an overlay so it does not shift existing page content
        self.page.overlay.append(self.picker)
        self.page.update()

        self.picker_button = OutlinedButton(
            "Choose .mp3 files...",
            on_click=lambda _: self.picker.pick_files(allow_multiple=True)
        )

        # begin with no files
        self.files = []
        self.file_number_reference.current.value = f"{len(self.files)} files selected"


    def on_file_picker_result(self, event: FilePickerResultEvent):
        if event.files is None:
            self.files = []
        else:
            self.files = event.files
        # make sure the page gets updated to display the newly selected files
        self.file_number_reference.current.value = f"{len(self.files)} files selected"
        self.page.update()
