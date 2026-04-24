import streamlit as st

crises_list = [
    "Drought in England",
    "Crop failure overseas",
    "Cyber attack",
    "Energy crunch"
    ]

response_list = [
    "Alternative fuels",
    "Emissions tax",
    "Integrated pest management",
    "Multi-trophic aquaculture",
    "Transition support fund"
    ]

def shock_menu_manager(shock):
    if shock == "Drought in England":
        opt1 = st.slider("Select the severity of the drought", 0, 10, 5)
        return([opt1])
    elif shock == "Crop failure overseas":
        opt1 = st.multiselect("Select the affected crops", ["Wheat", "Rice", "Maize", "Soy"])
        opt2 = st.slider("Select the severity of the crop failure", 0, 10, 5)
        return([opt1, opt2])
    elif shock == "Cyber attack":
        opt1 = st.slider("Select the severity of the cyber attack", 0, 10, 5)
        return([opt1])
    elif shock == "Energy crunch":
        opt1 = st.slider("Select the severity of the energy crunch", 0, 10, 5)
        return([opt1])
        