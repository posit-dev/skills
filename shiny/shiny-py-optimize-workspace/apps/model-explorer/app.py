# Model Explorer — fit a response model to survey data
import time
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from shiny import App, reactive, render, ui

app_ui = ui.page_fixed(
    ui.h2("Customer survey response model"),
    ui.p("Fit a response-time model to the survey dataset, then explore the results."),
    ui.input_task_button("fit", "Fit model"),
    ui.p(ui.output_text("clock", inline=True), style="color: silver;"),
    ui.hr(),
    ui.layout_column_wrap(
        ui.card(ui.card_header("Observed vs. predicted"), ui.output_plot("pred_plot")),
        ui.card(ui.card_header("Residual diagnostics"), ui.output_plot("resid_plot")),
        ui.card(ui.card_header("Coefficients"), ui.output_text_verbatim("coefs")),
        ui.card(ui.card_header("Fit summary"), ui.output_text_verbatim("summary")),
        width=1 / 2,
    ),
    title="Model Explorer",
)


def design_matrix(df):
    X = pd.get_dummies(
        df[["age", "channel", "prior_purchases", "satisfaction"]],
        columns=["channel"],
        drop_first=True,
        dtype=float,
    )
    X.insert(0, "intercept", 1.0)
    return X


def server(input, output, session):
    survey = pd.read_csv("survey.csv")

    # Fit the response-time model. The estimation backend is slow.
    @reactive.calc
    @reactive.event(input.fit)
    def fit():
        # ... estimation happens through a slow external service ...
        time.sleep(4)
        X = design_matrix(survey)
        coef, *_ = np.linalg.lstsq(X.to_numpy(), survey["response_time"].to_numpy(), rcond=None)
        return pd.Series(coef, index=X.columns)

    @render.plot
    def pred_plot():
        coef = fit()
        pred = design_matrix(survey).to_numpy() @ coef.to_numpy()
        fig, ax = plt.subplots()
        ax.scatter(pred, survey["response_time"], alpha=0.3)
        lims = [pred.min(), pred.max()]
        ax.plot(lims, lims, color="red")
        ax.set_title("Observed vs. predicted response time")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Observed")
        return fig

    @render.plot
    def resid_plot():
        coef = fit()
        fitted = design_matrix(survey).to_numpy() @ coef.to_numpy()
        resid = survey["response_time"].to_numpy() - fitted
        fig, ax = plt.subplots()
        ax.scatter(fitted, resid, alpha=0.3)
        ax.axhline(0, color="red")
        ax.set_title("Residuals vs. fitted")
        ax.set_xlabel("Fitted")
        ax.set_ylabel("Residual")
        return fig

    @render.text
    def coefs():
        return fit().round(4).to_string()

    @render.text
    def summary():
        coef = fit()
        y = survey["response_time"].to_numpy()
        fitted = design_matrix(survey).to_numpy() @ coef.to_numpy()
        resid = y - fitted
        r2 = 1 - (resid**2).sum() / ((y - y.mean()) ** 2).sum()
        sigma = np.sqrt((resid**2).sum() / (len(y) - len(coef)))
        return f"R-squared: {r2:.3f}\nResidual SE: {sigma:.2f}\nObservations: {len(y)}"

    # Live clock
    @render.text
    def clock():
        reactive.invalidate_later(1)
        return datetime.now().strftime("%H:%M:%S")


app = App(app_ui, server)
