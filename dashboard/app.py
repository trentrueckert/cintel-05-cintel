# --------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# --------------------------------------------

# From shiny, import just reactive and render
from shiny import reactive, render

# From shiny.express, import just ui and inputs if needed
from shiny.express import ui

# Imports from Python Standard Library to simulate live data
import random
from datetime import datetime
from collections import deque

# Import pandas for working with data
import pandas as pd

from faicons import icon_svg  

UPDATE_INTERVAL_SECS: int = 1

DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic
    temp = round(random.uniform(-18, -16), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"temp":temp, "timestamp":timestamp}

    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # For Display: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)

    # For Display: Get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry

    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, df, latest_dictionary_entry


ui.page_opts(title="PyShiny Express: Live Data With Value Card (Font Awesome Icon + 3 strings)", fillable=True)

with ui.sidebar(open="open"):

  ui.h2("Antarctic Explorer", class_="text-center")
  ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )
  ui.hr()
  ui.h6("Links:")
  ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-05-cintel-fancy",
        target="_blank",
  )
  ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-05-cintel-fancy/",
        target="_blank",
  )
  ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")

# In Shiny Express, everything not in the sidebar is in the main panel

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("sun"),
        theme="bg-gradient-blue-purple",
    ):

        "Current Temperature"

        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} C"

        "warmer than usual"

  

    with ui.card(full_screen=True):
        ui.card_header("Current Date and Time")

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"


with ui.layout_columns():
    with ui.card():
        ui.card_header("Current Data (placeholder only)")

with ui.layout_columns():
    with ui.card():
        ui.card_header("Current Chart (placeholder only)")