from textual.app import App

from pages.homepage import HomePage


class TrackTagger(App):
    CSS_PATH = "styles.css"

    def on_mount(self) -> None:
        self.install_screen(HomePage(), "home")
        app.push_screen("home")


if __name__ == "__main__":
    app = TrackTagger()
    app.run()
