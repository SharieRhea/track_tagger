import flet
from flet import (
    Page,
    Theme,
)
import logging
from pages.start import StartPage
from util.state import State

def main(page: Page):
    page.title = "track_tagger"
    page.padding = 16

    # create a random seed color and set the theme
    page.theme = Theme(color_scheme_seed=flet.Colors.random())

    state = State(page)
    page.on_resized = state.on_resized
    page.add(StartPage(state))

# enable logging
logging.basicConfig(level=logging.INFO)

flet.app(main)
