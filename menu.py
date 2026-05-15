import streamlit as st
from css_styles import css
from gui import custom_crisis_sandpit, crisis_from_database_dropdown, button_with_description, crisis_from_database_buttons
from widgets import collapsible_text
from display_shocks import altair_year_shock
import matplotlib.pyplot as plt
import numpy as np
st.html(css)

from streamlit_theme import st_theme
theme = st_theme()

if theme is not None:
    background_color = theme["backgroundColor"]
    secondary_background_color = theme["secondaryBackgroundColor"]

    plt.rcParams['axes.facecolor'] = secondary_background_color
    plt.rcParams['figure.facecolor'] = secondary_background_color
    plt.rcParams['axes.labelcolor'] = 'black'
    plt.rcParams['axes.titlecolor'] = 'black'
    plt.rcParams['xtick.color'] = 'black'
    plt.rcParams['ytick.color'] = 'black'
    plt.rcParams['text.color'] = 'black'

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

if "shock_sandpit_open" not in st.session_state:
    st.session_state["shock_sandpit_open"] = False

if "shock_database_open" not in st.session_state:
    st.session_state["shock_database_open"] = False

if "shock_dict" not in st.session_state:
    st.session_state["shock_dict"] = {}

st.logo(
    "https://www.aru.ac.uk/-/media/Images/234x234/logos/bafr-logo_234x234.jpg",
    size="large"
)

crisis_data = None

with st.sidebar:

    st.markdown(" ")
    st.title("BareFood Crisis Simulator")
    collapsible_text(
        """Welcome to the BareFood Crisis Simulator! This tool allows you to
        create and analyze various shocks that could impact the global food system.
        Use the buttons below to access the shock sandpit, where you can design your
        own shocks, or explore the shock database to see pre-defined shocks based on
        historical data and expert analysis. Lets get started and see how different
        shocks can affect our food system!""",
        key="welcome_text",)

    main_btn_cols = st.columns((2,3))

    with main_btn_cols[0]:
        if st.button("Shock sandpit", type="primary"):
            st.session_state["shock_sandpit_open"] = not st.session_state["shock_sandpit_open"]
            st.session_state["shock_database_open"] = False
            # st.rerun()
    
    with main_btn_cols[1]:
        if st.button("Open shock database", type="primary"):
            st.session_state["shock_database_open"] = not st.session_state["shock_database_open"]
            st.session_state["shock_sandpit_open"] = False
            # st.rerun()

    if st.session_state.shock_sandpit_open:
        crisis_data = custom_crisis_sandpit()

    elif st.session_state.shock_database_open:

        menu_mode = st.query_params.get("menu_mode", "dropdown")

        if menu_mode == "dropdown":
            crisis_data = crisis_from_database_dropdown()
        elif menu_mode == "buttons":
            crisis_data = crisis_from_database_buttons()
        else:
            st.error("Invalid menu mode. Please set 'menu_mode' query parameter to 'dropdown' or 'buttons'.")

    bot_container = st.container(vertical_alignment="bottom", height="stretch")
    with bot_container:
        st.button("Clear cache", on_click=lambda: st.cache_data.clear(), type="secondary")


col_shock_dict, col_display_shocks = st.columns([2,3], border=True)

with col_shock_dict:
    if st.session_state.shock_dict:
        st.write(st.session_state.shock_dict)

with col_display_shocks:
    if st.session_state.shock_dict:
        combined_chart = None

        for shock_data in st.session_state.shock_dict.values():
            c = altair_year_shock(shock_data)
            combined_chart = c if combined_chart is None else (combined_chart + c)

        st.altair_chart(
            combined_chart,
            width="stretch",
            height=600)