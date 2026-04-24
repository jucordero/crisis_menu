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
                    st.session_state.response_button_pressed = False

            with st.container(key="green_button"):
                response_button = st.button("Add new response", key="response_button")
                if response_button:
                    st.session_state.response_button_pressed = True
                    st.session_state.shock_button_pressed = False

            if st.session_state.shock_button_pressed:
                new_shock = st.selectbox("Select a shock", crises_list, index=None)
                if new_shock is not None:
                    with st.container(border=True):
                        shock_options = shock_menu_manager(new_shock)
                    add_new_shock = st.button("Add shock to dictionary", key="add_shock")
                    if add_new_shock:
                        st.session_state.shock_dict[new_shock] = shock_options
                        st.success(f"{new_shock} added to shock dictionary")

            if st.session_state.response_button_pressed:
                new_shock = st.selectbox("Select a response", response_list, index=None)
                add_new_response = st.button("Add response to dictionary", key="add_shock")
                if add_new_response:
                    st.session_state.shock_dict[new_shock] = []
                    st.success(f"{new_shock} added to shock dictionary")

st.write(st.session_state.shock_dict)