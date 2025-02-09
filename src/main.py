import flet
from flet import (
    Page,
    TemplateRoute,
    Theme,
    View,
)
import logging
from pages.start import StartPage
from pages.trackedit import TrackEditPage
from util.state import State

def main(page: Page):
    page.title = "track_tagger"
    page.padding = 16

    # create a random seed color and set the theme
    page.theme = Theme(color_scheme_seed=flet.Colors.random())

    state = State(page)
    page.on_resized = state.on_resized
    page.on_route_change = lambda _: on_route_change(page, state)

    # initialize the default route
    state.page.views.append(View("/start", [StartPage(state)]))

    page.go("/start")

def on_route_change(page: Page, state: State):
    route = TemplateRoute(page.route)
    if route.match("/start"):
        page.views.clear()
        page.views.append(View("/start", [StartPage(state)]))
        state.clear()
        page.go("/start")
    elif route.match("/trackedit"):
        page.views.clear()
        page.views.append(View("/trackedit", [TrackEditPage(state)]))
        page.go("/trackedit")
    page.update()

# enable logging
logging.basicConfig(level=logging.INFO)

flet.app(main)
