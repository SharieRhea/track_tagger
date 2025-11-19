import logging
import os
from pathlib import Path
from typing import List

from rich.style import Style
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.logging import TextualHandler
from textual.screen import Screen
from textual.widgets import Button, DirectoryTree, Footer
from textual.widgets.tree import TreeNode

from pages.editpage import EditPage

logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
)


class FileSelectPage(Screen):

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        self.add_class("center")
        self.filetree = DirectoryTree(".", id="file-select", classes="round-border")
        self.filetree.border_title = "select music files to edit:"
        # stop "enter" from expanding/collapsing dirs
        self.filetree.auto_expand = False
        self.selected_files: List[Path] = []

        yield self.filetree
        yield Button("continue", id="continue-button", variant="primary", flat=True)
        yield Footer()

    # FIX: weird behavior with selecting a dir, sometimes takes two key presses
    # NOTE: what's happening here is the files within a directory are not loaded by textual until you expand the directory node itself
    # possible fix might be to manually "expand and hide" when user presses enter
    @on(DirectoryTree.DirectorySelected)
    def on_directorytree_directoryselected(self, event: DirectoryTree.DirectorySelected) -> None:
        # NOTE: i am choosing to not traverse subdirectories here
        file_nodes = [child for child in event.node.children if not child.allow_expand]
        file_paths = [Path(self.retrieve_full_path(node, "")) for node in file_nodes]
        if all(path in self.selected_files for path in file_paths):
            # all the files in this dir were selected, deselect them all
            for node in file_nodes:
                self.selected_files.remove(Path(self.retrieve_full_path(node, "")))
                styled_label = Text(str(node.label), Style())
                node.set_label(styled_label)
            # deselect the dir itself
            styled_label = Text(str(event.node.label), Style())
            event.node.set_label(styled_label)
        else:
            # some (or no) files have already been selected, select the remaining ones
            for index, node in enumerate(file_nodes):
                if file_paths[index] not in self.selected_files:
                    self.selected_files.append(file_paths[index])
                    styled_label = Text(str(node.label), Style(bgcolor=self.app.theme_variables["primary-background"]))
                    node.set_label(styled_label)
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
            styled_label = Text(
                str(fileselected.node.label), Style(bgcolor=self.app.theme_variables["primary-background"])
            )
        fileselected.node.set_label(styled_label)

    @on(Button.Pressed)
    def on_button_pressed(self, _: Button.Pressed) -> None:
        self.app.install_screen(EditPage(self.selected_files), "edit")
        self.app.push_screen("edit")

    def retrieve_full_path(self, node: TreeNode, path: str) -> str:
        # TODO: this may need to be modified to work when the user has a configured default directory

        # prepend this node's label to what we have so far
        path = os.path.join(str(node.label), path)

        if node.is_root or not node.parent:
            if isinstance(node.tree, DirectoryTree):
                # build the full absolute path
                tree_path = Path(node.tree.path).resolve()
                return os.path.join(tree_path, path)
            else:
                raise Exception("TreeNode root was not a DirectoryTree instance! Unable to retrieve path.")
        # recursively walk up the tree
        return self.retrieve_full_path(node.parent, path)
