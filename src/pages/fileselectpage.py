from pathlib import Path
from typing import List
from rich.style import Style
from rich.text import Text
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
        # NOTE: i am choosing to not traverse subdirectories here

        # TODO: this needs to select remaining if only some are selected, also the highlight of the directory itself needs to make sense
        for node in [child for child in event.node.children if not child.allow_expand]:
            path = Path(str(node.label))
            if path in self.selected_files:
                self.selected_files.remove(path)
                styled_label = Text(str(node.label), Style())
            else:
                self.selected_files.append(path)
                styled_label = Text(str(node.label), Style(bgcolor=self.app.current_theme.accent))
            node.set_label(styled_label)

    @on(DirectoryTree.FileSelected)
    def on_directorytree_fileselected(self, fileselected: DirectoryTree.FileSelected) -> None:
        if fileselected.path in self.selected_files:
            self.selected_files.remove(fileselected.path)
            styled_label = Text(str(fileselected.node.label), Style())
        else:
            self.selected_files.append(fileselected.path)
            styled_label = Text(str(fileselected.node.label), Style(bgcolor=self.app.current_theme.accent))
        fileselected.node.set_label(styled_label)

    @on(Button.Pressed)
    def on_button_pressed(self, _: Button.Pressed) -> None:
        self.app.install_screen(EditPage(self.selected_files[0]), "edit")
        self.app.push_screen("edit")
