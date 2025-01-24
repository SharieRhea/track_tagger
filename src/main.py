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
    page.add(StartPage(state))

# enable logging
logging.basicConfig(level=logging.INFO)

flet.app(main)
