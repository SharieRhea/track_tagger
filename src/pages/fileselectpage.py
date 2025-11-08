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
        # stop "enter" from expanding/collapsing dirs
        self.filetree.auto_expand = False
        self.selected_files: List[Path] = []
        yield self.filetree
        yield Button("continue")

    # FIX: weird behavior with selecting a dir, sometimes takes two key presses
    @on(DirectoryTree.DirectorySelected)
    def on_directorytree_directoryselected(self, event: DirectoryTree.DirectorySelected) -> None:
        # NOTE: i am choosing to not traverse subdirectories here
        file_nodes = [child for child in event.node.children if not child.allow_expand]
        if all(Path(str(node.label)) in self.selected_files for node in file_nodes):
            # all the files in this dir were selected, deselect them all
            for node in file_nodes:
                self.selected_files.remove(Path(str(node.label)))
                styled_label = Text(str(node.label), Style())
                node.set_label(styled_label)
            # deselect the dir itself
            styled_label = Text(str(event.node.label), Style())
            event.node.set_label(styled_label)
        else:
            # some (or no) files have already been selected, select the remaining ones
            for remaining_node in [node for node in file_nodes if node not in self.selected_files]:
                self.selected_files.append(Path(str(remaining_node.label)))
                styled_label = Text(str(remaining_node.label), Style(bgcolor=self.app.theme_variables["primary-background"]))
                remaining_node.set_label(styled_label)
            # select the dir itself
            styled_label = Text(str(event.node.label), Style(bgcolor=self.app.theme_variables["primary-background"]))
            event.node.set_label(styled_label)

    @on(DirectoryTree.FileSelected)
    def on_directorytree_fileselected(self, fileselected: DirectoryTree.FileSelected) -> None:
        if fileselected.path in self.selected_files:
            self.selected_files.remove(fileselected.path)
            styled_label = Text(str(fileselected.node.label), Style())
            # we are removing a file from the selection, this means its parent dir has at least one file unselected
            # therefore, update so the dir is deselected (if it wasn't already)
            dir_node = fileselected.node.parent
            if dir_node:
                dir_label = Text(str(dir_node.label), Style())
                dir_node.set_label(dir_label)
        else:
            self.selected_files.append(fileselected.path)
            styled_label = Text(str(fileselected.node.label), Style(bgcolor=self.app.theme_variables["primary-background"]))
        fileselected.node.set_label(styled_label)

    @on(Button.Pressed)
    def on_button_pressed(self, _: Button.Pressed) -> None:
        self.app.install_screen(EditPage(self.selected_files[0]), "edit")
        self.app.push_screen("edit")
