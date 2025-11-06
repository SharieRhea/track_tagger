from pathlib import Path
from typing import List
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, DirectoryTree

from pages.editpage import EditPage


class FileSelectPage(Screen):

    def __init__(self):
        super().__init__()
        

    def compose(self) -> ComposeResult:
        self.filetree = DirectoryTree(".")
        self.selected_files: List[Path] = []
        yield self.filetree
        yield Button("continue")


    @on(DirectoryTree.DirectorySelected)
    def on_directorytree_directoryselected(self, event: DirectoryTree.DirectorySelected) -> None:
        # retrieve only FILES from this directory and add them to the selection
        # NOTE: i am choosing to not traverse subdirectories here
        for file in event.path.glob("*"):
            if not Path.is_dir(file):
                self.selected_files.append(file)

    @on(DirectoryTree.FileSelected)
    def on_directorytree_fileselected(self, fileselected: DirectoryTree.FileSelected) -> None:
        self.selected_files.append(fileselected.path)
        # TODO: highlight the selected file

    @on(Button.Pressed)
    def on_button_pressed(self, _: Button.Pressed) -> None:
        self.app.install_screen(EditPage(self.selected_files[0]), "edit")
        self.app.push_screen("edit")
