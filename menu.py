import streamlit as st
from css_styles import css
from shock_menus import crises_list, response_list, shock_menu_manager
import matplotlib.pyplot as plt
import numpy as np
st.html(css)


from streamlit_theme import st_theme
theme = st_theme()
if theme is not None:
    background_color = theme["backgroundColor"]
plt.rcParams['axes.facecolor'] = background_color
plt.rcParams['figure.facecolor'] = background_color
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['axes.titlecolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['text.color'] = 'white'

model_years = np.arange(2025, 2101)  # Define the range of years

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
        sand_pit_container = st.container(border=True)
        with sand_pit_container:
            for shock_name, shock_info in st.session_state.shock_dict.items():
                cols_list_shocks = st.columns(2)
                with cols_list_shocks[0]:
                    st.write(f"Shock name: {shock_name}")
                with cols_list_shocks[1]:
                    delete_button = st.button("Delete shock", key=f"delete_{shock_name}")
                    if delete_button:
                        del st.session_state.shock_dict[shock_name]
                        st.success(f"Shock {shock_name} deleted")
                        st.rerun()

            with st.container(key="red_button"):
                shock_button = st.button("Add new shock", key="shock_button")
                if shock_button:
                    st.session_state.shock_button_pressed = True

            if st.session_state.shock_button_pressed:
                
                plot_cont = st.container(key="shock_plot")
                severity = np.zeros(len(model_years))
                
                  # Initialize year as an empty array
                element = st.multiselect(
                    "Select an element of the food system",
                    ["Production", "Imports", "Exports", "Retail", "Seed", "Feed", "Stocks"],
                    help="Specify which element(s) of the food system are impacted")
                items = st.multiselect(
                    "Select the items that are affected",
                    ["Wheat", "Maize", "Rice", "Soybeans", "Other"],
                    help="Specify which food items or food item groups are is impacted")
                profile = st.selectbox(
                    "Select the timescale of the shock",
                    ["Single year", "Continuous", "Gradual"],
                    help = """Specify the time profiling of the perturbation.
                        Choose from 
                        ‘Single year’: the perturbation only affects the individual year(s) selected; 
                        ‘Continuous’: the perturbation starts at the selected year and continues for all years following that
                        ‘Gradual’: the perturbation is smoothly changing (logistic curve)""")
                
                if profile == "Single year":
                    shock_year = st.slider("Select the year when the shock happens", 2025, 2100, 2025, step=1)

                if profile == "Continuous":
                    shock_year = st.slider("Select the starting year of the shock", 2025, 2100, 2025, step=1)

                if profile == "Gradual":
                    with st.container(border=True):
                        log_center = st.slider("Select the central year of the logistic curve", 2025, 2100, 2025, step=1)
                        log_width = st.slider("Select width of the logistic curve ", 1, 20, 5, step=1)

                severity_slider = st.slider(
                    "Select the percentage change",
                    -100, 100, 0, step=10)

                if profile == "Single year":
                    severity[model_years == shock_year] = severity_slider
                elif profile == "Continuous":
                    severity[model_years >= shock_year] = severity_slider
                elif profile == "Gradual":
                    severity = severity_slider / (1 + np.exp(-(model_years - log_center) / log_width))

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
                        
                name = st.text_input("Name the shock", help="Give a name to the shock you want to add")

                with plot_cont:
                    fig, ax = plt.subplots()
                    ax.plot(model_years, severity)
                    ax.set_xlabel("Year")
                    ax.set_ylabel("Shock severity (%)")
                    ax.set_title("Shock profile over time")
                    st.pyplot(fig)

                button_cols = st.columns(2)
                with button_cols[0]:
                    submit_button = st.button("Submit shock", key="submit_shock")
                    st.checkbox("Submit to shock database", key="submit_to_db")
                    if submit_button:
                        st.session_state.shock_dict[name] = {
                            "element": element,
                            "items": items,
                            "severity": severity,
                            "area": area,
                            "region": region
                        }
                        # st.session_state.shock_button_pressed = False
                        with sand_pit_container:
                            st.success(f"Shock {name} submitted")
                        # st.rerun()

                with button_cols[1]:
                    reset_shocks = st.button("Reset shocks", key="reset_shocks")
                    if reset_shocks:
                        st.session_state.shock_dict = {}
                        # st.session_state.shock_button_pressed = False
                        with sand_pit_container:
                            st.success("Shocks reset")
                        # st.rerun()

                

                


# st.write(st.session_state.shock_dict)

fig, ax = plt.subplots()

for shock_name, shock_info in st.session_state.shock_dict.items():
    ax.plot(model_years, shock_info["severity"], label=shock_name)

ax.legend()
ax.set_ylabel("Shock severity (%)")
ax.set_xlabel("Year")
st.pyplot(fig)
