# Deterministic data generator for the sales-dashboard fixture.
# Run from this directory: python generate_data.py  (writes sales.csv here)
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

regions = ["North", "South", "East", "West"]
base_cities = {"North": "Springfield", "South": "Riverton", "East": "Laketown", "West": "Hillcrest"}
products = ["Widget", "Gadget", "Doohickey", "Contraption", "Gizmo", "Thingamajig"]
categories = ["Hardware", "Software", "Services"]
dates = pd.date_range("2019-01-01", "2023-12-31", freq="D")

n_per_region = 50_000  # 4 regions x 50k = 200k rows


def make_region(region: str, n: int) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": rng.choice(dates, n),
            "region": region,
            "city": [f"{base_cities[region]} {i}" for i in rng.integers(1, 4, n)],
            "product": rng.choice(products, n),
            "category": rng.choice(categories, n, p=[0.5, 0.3, 0.2]),
            "units": rng.integers(1, 21, n),
        }
    )


sales = pd.concat([make_region(r, n_per_region) for r in regions], ignore_index=True)

# Revenue with mild seasonality + noise; deterministic given the seed
doy = sales["date"].dt.day_of_year.to_numpy()
sales["revenue"] = np.round(
    sales["units"] * (50 + 10 * np.sin(2 * np.pi * doy / 365) + rng.normal(0, 5, len(sales))),
    2,
)

sales = sales.sort_values("date", kind="stable")
sales["date"] = sales["date"].dt.strftime("%Y-%m-%d")
sales.to_csv("sales.csv", index=False)
print(f"wrote sales.csv with {len(sales)} rows")
