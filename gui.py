import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import gspread
from urllib.parse import urlencode
from widgets import button_with_description, collapsible_text
from database import get_all_crisis_descriptions, get_crisis_data, write_crisis_to_database
from lists import *


def custom_crisis_sandpit(
    name=None,
    long_description=None,
    shock_type=None,
    element=None,
    items=None,
    profile=None,
    shock_year=None,
    log_width=None,
    severity=None,
    region=None,
    border=True,
    allow_subit=True
):

    sand_pit_container = st.container(border=border)
    with sand_pit_container:
        col_name, col_type = st.columns(2)

        # Name
        with col_name:
            name = st.text_input(
                "Name the shock",
                value=name if name else "",
                help="Give a name to the shock you want to add")
            
        # Type
        with col_type:
            shock_type = st.selectbox(
                "Type of shock",
                ["Crisis", "Intervention"],
                index=None if shock_type is None else ["Crisis", "Intervention"].index(shock_type),
                help="Select the type of shock you want to add",
            )

        # Long description
        long_description = st.text_area(
            "Describe the shock in more detail",
            value=long_description if long_description else "",
            height="content",
            help="Provide a detailed description of the shock, including its causes, impacts, and any other relevant information.")

        # Elements
        element = st.multiselect(
            "Select impacted elements of the food system",
            element_list,
            default=element if element else [],
            help="Specify which element(s) of the food system are impacted")
        
        # Items
        items = st.multiselect(
            "Select the items that are affected",
            item_list,
            default=items if items else [],
            help="Specify which food items or food item groups are is impacted")
        
        # Temporal profile
        profile = st.selectbox(
            "Select the timescale of the shock",
            profile_list,
            index=None if profile is None else profile_list.index(profile),
            help="""Specify the time profiling of the perturbation.
                Choose from 
                'Single year': the perturbation only affects the individual year(s) selected; 
                'Continuous': the perturbation starts at the selected year and continues for all years following that
                'Gradual': the perturbation is smoothly changing (logistic curve)""")

        if profile == "Single year":
            shock_year = st.slider(
                "Select the year when the shock happens",
                min_value=2025,
                max_value=2100,
                value=shock_year if shock_year else 2025,
                step=1)
            
            log_width = 0  # Not applicable for single year shocks

        if profile == "Continuous":
            with st.container(border=True):
                shock_year = st.slider(
                    "Select the starting year of the shock",
                    min_value=2025,
                    max_value=2100,
                    value=shock_year if shock_year else 2025,
                    step=1)
                    
                log_width = st.slider(
                    "Select duration of the shock",
                    min_value=1,
                    max_value=2100 - shock_year,
                    value = log_width if log_width else 5,
                    step=1)

        if profile == "Gradual":
            with st.container(border=True):
                shock_year = st.slider(
                    "Select the central year of the logistic curve",
                    min_value=2025,
                    max_value=2100,
                    value=shock_year if shock_year else 2025,
                    step=1)
                
                log_width = st.slider(
                    "Select width of the logistic curve ",
                    min_value=1,
                    max_value=20,
                    value = log_width if log_width else 5,
                    step=1)

        # Severity
        severity = st.slider(
            "Select the percentage change",
            min_value=-100,
            max_value=100,
            value=severity if severity else 0,
            step=10
        )

        # Geographical extent
        region = st.multiselect(
            "Select the region affected",
            region_list,
            default=region if region else [],
            help="Specify the geographical region affected by the shock")
        
        if allow_subit:
            submit_to_database = st.checkbox("Submit to database")
        else:
            submit_to_database = False

        submit_button = st.button("Submit shock", key="submit_shock")

        if submit_button:
            crisis_data = {
                "name": name,
                "description": long_description,
                "type": shock_type,
                "element": element,
                "items": items,
                "timescale": profile,
                "year": shock_year,
                "width": log_width,
                "severity": severity,
                "region": region,
            }

            if submit_to_database:
                write_crisis_to_database(crisis_data)
                st.success("Shock submitted to database!")

            st.session_state.shock_dict[name] = crisis_data

            return crisis_data


def crisis_from_database_dropdown():
    """Displays a selectbox with crisis labels from the database,
    and shows the description of the selected crisis."""
    crisis_labels, crisis_descriptions = get_all_crisis_descriptions()

    crisis_database_container = st.container(border=True)
    with crisis_database_container:

        crisis_sel_col, clear_cache_col = st.columns([4,1], vertical_alignment="bottom")
        with crisis_sel_col:
            selected_crisis = st.selectbox(
                "Select a shock from the database",
                crisis_labels,
                index=None,
                help="Select a shock from the database to add it to the sandpit")

        with clear_cache_col:
            st.button(
                "",
                on_click=lambda: st.session_state.update({"shock_dict": {}}),
                type="secondary",
                icon=":material/autorenew:")

        if selected_crisis is not None:
            # crisis_index = crisis_labels.index(selected_crisis)
            crisis_data = get_crisis_data(selected_crisis)

            st.divider()

            crisis_data = custom_crisis_sandpit(
                name=crisis_data["name"],
                long_description=crisis_data["description"],
                shock_type=crisis_data["type"],
                element=crisis_data["element"],
                items=crisis_data["items"],
                profile=crisis_data["timescale"],
                shock_year=crisis_data["year"],
                log_width=crisis_data["width"],
                severity=crisis_data["severity"],
                region=crisis_data["region"],
                border=False,
                allow_subit=False
                )

            return crisis_data

def crisis_from_database_buttons():
    """Displays buttons with crisis labels and descriptions from the database, 
    using the button_with_description widget."""

    crisis_labels, crisis_descriptions = get_all_crisis_descriptions()

    cont = st.container(border=True, height=680)
    with cont:
        crisis_button_array = [button_with_description(
            label, description) for label, description in zip(crisis_labels, crisis_descriptions)]

    for i, crisis_button in enumerate(crisis_button_array):
        if crisis_button:
            selected_crisis = crisis_labels[i]
            st.success(f"'{selected_crisis}' added to model.")
            crisis_data = get_crisis_data(selected_crisis)
            return crisis_data



