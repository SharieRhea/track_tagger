from typing import Iterable

from textual.app import App, SystemCommand
from textual.screen import Screen

from pages.fileselectpage import FileSelectPage
from pages.settingspage import SettingsPage


class TrackTagger(App):
    CSS_PATH = "styles.css"
    COMMAND_PALETTE_BINDING = "ctrl+backslash"

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)
        yield SystemCommand("Settings", "Change the app settings", lambda: app.push_screen("settings"))

    def on_mount(self) -> None:
        # TODO: if there is no configuration file present (or it's completely blank), open to settings
        self.install_screen(SettingsPage(), "settings")
        self.install_screen(FileSelectPage(), "file_select")
        app.push_screen("file_select")


if __name__ == "__main__":
    app = TrackTagger()
    app.run()
