import flet
from flet import (
    Page,
)
import logging
from pages.start import StartPage
from util.state import State

def main(page: Page):
    page.title = "track_tagger"
    page.padding = 16

    state = State(page)

    app = StartPage(state)
    page.add(app)
    page.update()

# enable logging
logging.basicConfig(level=logging.INFO)

flet.app(main)
