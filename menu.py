import streamlit as st
from css_styles import css
from shock_menus import crises_list, response_list, shock_menu_manager
st.html(css)

if "shock_sandpit_open" not in st.session_state:
    st.session_state["shock_sandpit_open"] = False

if "shock_dict" not in st.session_state:
    st.session_state["shock_dict"] = {}

if "shock_button" not in st.session_state:
    st.session_state["shock_button_pressed"] = False

if "response_button" not in st.session_state:
    st.session_state["response_button_pressed"] = False

with st.sidebar:
    if st.button("Shock sandpit", type="primary"):
        st.session_state["shock_sandpit_open"] = ~st.session_state["shock_sandpit_open"]

    if st.session_state.shock_sandpit_open:
        with st.container(border=True):
            with st.container(key="red_button"):
                shock_button = st.button("Add new shock", key="shock_button")
                if shock_button:
                    st.session_state.shock_button_pressed = True

            if st.session_state.shock_button_pressed:
                name = st.text_input("Name the shock", help="Give a name to the shock you want to add")
                element = st.multiselect(
                    "Select an element of the food system",
                    ["Production", "Imports", "Exports", "Retail", "Seed", "Feed", "Stocks"],
                    help="Specify which element(s) of the food system are impacted")
                items = st.multiselect(
                    "Select the items that are affected",
                    ["Wheat", "Maize", "Rice", "Soybeans", "Other"],
                    help="Specify which food items or food item groups are is impacted")
                timescale = st.selectbox(
                    "Select the timescale of the shock",
                    ["Single year", "Continuous", "Gradual"],
                    help = """Specify the time profiling of the perturbation.
                        Choose from 
                        ‘Single year’: the perturbation only affects the individual year(s) selected; 
                        ‘Continuous’: the perturbation starts at the selected year and continues for all years following that
                        ‘Gradual’: the perturbation is smoothly changing (logistic curve)""")
                
                if timescale == "Single year":
                    st.slider("Select the year when the shock happens", 2025, 2100, 2025, step=1)

                if timescale == "Continuous":
                    st.slider("Select the starting year of the shock", 2025, 2100, 2025, step=1)

                if timescale == "Gradual":
                    with st.container(border=True):
                        st.slider("Select the central year of the logistic curve", 2025, 2100, 2025, step=1)
                        st.slider("Select width of the logistic curve ", 1, 20, 5, step=1)

                severity = st.slider(
                    "Select the percentage change",
                    -100, 100, 0, step=10)
                col_area = st.columns(2)
                with col_area[0]:
                    area = st.selectbox(
                        "Select the area affected",
                        ["Country", "Region"])
                with col_area[1]:
                    if area == "Country":
                        region = st.selectbox(
                            "Select the country affected",
                            ["Scotland", "England", "Ireland", "Wales"])
                    elif area == "Region":
                        region = st.multiselect(
                            "Select the region affected",
                            ["North", "South", "East", "West"])
                        

                button_cols = st.columns(2)
                with button_cols[0]:
                    submit_button = st.button("Submit shock", key="submit_shock")
                    if submit_button:
                        st.session_state.shock_dict[name] = {
                            "element": element,
                            "items": items,
                            "timescale": timescale,
                            "severity": severity,
                            "area": area,
                            "region": region
                        }
                        st.session_state.shock_button_pressed = False
                        st.success(f"Shock {name} submitted")
                        st.rerun()
                with button_cols[1]:
                    reset_shocks = st.button("Reset shocks", key="reset_shocks")
                    if reset_shocks:
                        st.session_state.shock_dict = {}
                        st.session_state.shock_button_pressed = False
                        st.success("Shocks reset")
                        st.rerun()


st.write(st.session_state.shock_dict)