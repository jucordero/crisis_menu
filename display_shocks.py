import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import pandas as pd

def altair_year_shock(shock_data):
    """Displays the shock data using altair.
    
    The shock_data is expected to be a dictionary with keys 'name', 'type',
    'element', 'severity' and temporaly profile information (e.g. 'year',
    'width' for gradual shocks). It returns a chart with severity plotted over
    time."""

    model_years = np.arange(2025, 2101, dtype=int)
    severity_over_time = np.zeros_like(model_years, dtype=float)
    name = [shock_data.get("name", "Unnamed Shock")]*len(model_years)

    if shock_data["timescale"] == "Gradual":
        # For a gradual shock, we can model it as a logistic curve centered around the shock year
        shock_year = shock_data["year"]
        width = shock_data["width"]
        severity = shock_data["severity"]
        severity_over_time = severity * (1 / (1 + np.exp(-(model_years - shock_year) / width)))

    elif shock_data["timescale"] == "Single year":
        # For a single year shock, we can model it as a spike in severity at the shock year
        shock_year = shock_data["year"]
        severity = shock_data["severity"]
        severity_over_time = np.where(model_years == shock_year, severity, 0)

    elif shock_data["timescale"] == "Continuous":
        # For a continuous shock, we can model it as a constant severity starting from the shock year
        shock_year = shock_data["year"]
        severity = shock_data["severity"]
        width = shock_data.get("width", np.inf)
        severity_over_time = np.where((model_years >= shock_year) & (model_years <= shock_year + width), severity, 0)

    df = pd.DataFrame({
        'Year': model_years,
        'Severity': severity_over_time,
        'Name': name
    })

    # import random
    # random_color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
    
    chart = alt.Chart(df).mark_area().encode(
        x=alt.X('Year:O', axis=alt.Axis(values = [2025, 2050, 2075, 2100])),
        y=alt.Y('Severity', scale=alt.Scale(domain=[-100, 100])),
        tooltip=['Name', 'Year', 'Severity'],
        opacity=alt.value(0.6)
    )
    
    return chart