# Sales Dashboard — regional revenue explorer
import matplotlib.pyplot as plt
import pandas as pd
import time

from shiny import render, ui
from shiny.express import input, ui as xui
from shiny import reactive

PRODUCTS = ["Widget", "Gadget", "Doohickey", "Contraption", "Gizmo", "Thingamajig"]

sales = pd.read_csv("sales.csv")

# Some prep work
sales["month"] = pd.to_datetime(sales["date"]).dt.to_period("M").dt.to_timestamp()
sales["year"] = pd.to_datetime(sales["date"]).dt.year

xui.page_opts(title="Sales Dashboard", fillable=False)

with xui.sidebar():
    ui.input_select("region", "Region", ["All", "North", "South", "East", "West"])
    ui.input_slider("year", "Year range", 2019, 2023, value=(2019, 2023), step=1, sep="")

    # The city list depends on the region
    @render.ui
    def city_ui():
        if input.region() == "All":
            cities = sorted(sales["city"].unique())
        else:
            cities = sorted(sales.loc[sales["region"] == input.region(), "city"].unique())
        return ui.input_select("city", "City", ["All", *cities])

    ui.input_selectize("product", "Product", PRODUCTS, selected=PRODUCTS, multiple=True)


# Helper for filtering
def filter_sales(df):
    if input.region() != "All":
        df = df[df["region"] == input.region()]
    lo, hi = input.year()
    df = df[(df["year"] >= lo) & (df["year"] <= hi)]
    if input.city() != "All":
        df = df[df["city"] == input.city()]
    df = df[df["product"].isin(input.product())]
    return df


with xui.layout_column_wrap(width=1 / 2):
    with xui.card():
        xui.card_header("Monthly revenue")

        @render.plot
        def revenue_plot():
            d = filter_sales(sales)
            agg = d.groupby("month")["revenue"].sum()
            fig, ax = plt.subplots()
            ax.plot(agg.index, agg.values, color="steelblue", linewidth=1)
            ax.set_title("Monthly revenue")
            ax.set_ylabel("Revenue ($)")
            return fig

    with xui.card():
        xui.card_header("Revenue summary")

        @render.code
        def revenue_summary():
            d = filter_sales(sales)
            total = d["revenue"].sum()
            avg = d["revenue"].mean()
            n = len(d)
            return f"Total revenue: ${total:.0f}\nAverage per sale: ${avg:.2f}\nNumber of sales: {n}"

    with xui.card():
        xui.card_header("Top products")

        @render.plot
        def top_products():
            d = filter_sales(sales)
            agg = d.groupby("product")["revenue"].sum().sort_values(ascending=False).iloc[:6]
            fig, ax = plt.subplots()
            ax.barh(agg.index[::-1], agg.values[::-1], color="darkorange")
            ax.set_title("Top products by revenue")
            ax.set_xlabel("Revenue ($)")
            return fig

    with xui.card():
        xui.card_header("Category mix")

        @render.plot
        def category_mix():
            d = filter_sales(sales)
            agg = d.groupby("category")["revenue"].sum()
            fig, ax = plt.subplots()
            ax.pie(agg.values, labels=agg.index)
            ax.set_title("Revenue by category")
            return fig

    with xui.card():
        xui.card_header("Store detail (scatter)")

        @render.plot
        def store_scatter():
            d = filter_sales(sales)
            fig, ax = plt.subplots()
            ax.scatter(d["units"], d["revenue"], alpha=0.4)
            ax.set_title("Units vs. revenue")
            ax.set_xlabel("Units")
            ax.set_ylabel("Revenue ($)")
            return fig

    # Compare with competitor benchmark data from our market research API
    @reactive.calc
    def benchmark_data():
        time.sleep(1.5)  # the market research API is slow
        return pd.DataFrame(
            {
                "product": PRODUCTS,
                "competitor_avg": [120000, 95000, 88000, 61000, 45000, 31000],
            }
        )

    with xui.card():
        xui.card_header("Benchmark vs. competitors")

        @render.plot
        def benchmark_plot():
            d = filter_sales(sales)
            ours = d.groupby("product", as_index=False)["revenue"].sum()
            combined = ours.merge(benchmark_data(), on="product", how="outer")
            combined = combined.rename(columns={"revenue": "ours"}).fillna({"ours": 0})
            fig, ax = plt.subplots()
            ax.barh(combined["product"], combined["ours"], label="Ours")
            ax.barh(combined["product"], combined["competitor_avg"], alpha=0.5, label="Competitor avg")
            ax.set_title("Revenue vs. competitor benchmark")
            ax.set_xlabel("Revenue ($)")
            ax.legend()
            return fig

    with xui.card():
        xui.card_header("Detail table")

        @render.table
        def detail_table():
            d = filter_sales(sales)
            return d[["date", "region", "city", "product", "category", "units", "revenue"]]
