# Ops Monitor — live order volume plus an on-demand incident report
import asyncio
import random
from datetime import datetime

from shiny import App, reactive, render, ui

SERVICES = ["checkout", "search", "payments", "inventory"]

app_ui = ui.page_fixed(
    ui.h2("Ops monitor"),
    ui.p(ui.output_text("clock", inline=True), style="color: silver;"),
    ui.input_select("service", "Service", SERVICES),
    ui.input_action_button("refresh", "Refresh incident report"),
    ui.hr(),
    ui.layout_column_wrap(
        ui.card(ui.card_header("Live order volume"), ui.output_text_verbatim("volume")),
        ui.card(ui.card_header("Incident report"), ui.output_text_verbatim("report")),
        width=1 / 2,
    ),
    title="Ops Monitor",
)


async def fetch_incident_report(service: str) -> str:
    # The incident API is slow; it can take several seconds to answer.
    await asyncio.sleep(5)
    n = random.randint(0, 4)
    return f"{service}: {n} open incident(s) as of {datetime.now():%H:%M:%S}"


def server(input, output, session):
    latest_volume = reactive.value(0)
    incident_report = reactive.value("Click refresh to load the report.")

    # Feed order volume from a background task. It runs outside the reactive
    # graph, so take the lock and flush so the outputs update.
    async def poll_volume():
        while True:
            await asyncio.sleep(2)
            async with reactive.lock():
                latest_volume.set(random.randint(800, 1200))
                await reactive.flush()

    poller = asyncio.create_task(poll_volume())
    session.on_ended(poller.cancel)

    # Async so the slow API call doesn't block the app.
    @reactive.effect
    @reactive.event(input.refresh)
    async def _():
        incident_report.set(await fetch_incident_report(input.service()))

    @render.text
    def volume():
        return f"{input.service()}: {latest_volume()} orders/min"

    @render.text
    def report():
        return incident_report()

    @render.text
    def clock():
        reactive.invalidate_later(1)
        return datetime.now().strftime("%H:%M:%S")


app = App(app_ui, server)
