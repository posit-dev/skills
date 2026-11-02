# Deterministic data generator for the model-explorer fixture.
# Run from this directory: python generate_data.py  (writes survey.csv here)
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 30_000

channels = ["email", "phone", "chat", "web"]
survey = pd.DataFrame(
    {
        "age": rng.integers(18, 80, n),
        "channel": rng.choice(channels, n),
        "prior_purchases": rng.poisson(3, n),
        "satisfaction": rng.integers(1, 6, n),
    }
)
channel_effect = survey["channel"].map({"email": 0, "phone": -4, "chat": -6, "web": 2})
survey["response_time"] = np.round(
    40
    + 0.2 * survey["age"]
    - 1.5 * survey["prior_purchases"]
    - 2 * survey["satisfaction"]
    + channel_effect
    + rng.normal(0, 8, n),
    2,
)

survey.to_csv("survey.csv", index=False)
print(f"wrote survey.csv with {len(survey)} rows")
