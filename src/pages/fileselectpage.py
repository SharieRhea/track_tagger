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
        yield self.filetree
        yield Button("continue")


    @on(DirectoryTree.FileSelected)
    def on_directorytree_fileselected(self, fileselected: DirectoryTree.FileSelected) -> None:
        self.app.install_screen(EditPage(str(fileselected.path)), "edit")
        self.app.push_screen("edit")
