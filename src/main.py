import flet
from flet import (
    Page,
)
import logging
from pages.start import StartPage

def main(page: Page):
    page.title = "track_tagger"
    page.padding = 16

    app = StartPage(page)
    page.add(app)
    page.update()

# enable logging
logging.basicConfig(level=logging.INFO)

flet.app(main)
