import streamlit as st

@st.fragment
def collapsible_text(
        text,
        key,
        max_chars=100,
        expanded=False,
    ):
    """Creates a collapsible text element with a "Show more" button if the text
    exceeds a specified character limit."""

    if f"{key}_expanded" not in st.session_state:
        st.session_state[f"{key}_expanded"] = expanded

    if len(text) <= max_chars:
        st.markdown(":small["+text+"]")
        return
    
    else:
        if st.session_state[f"{key}_expanded"]:
            st.caption(":small["+ text + "]")
            if st.button("Show less", key=f"{key}_collapse", type="tertiary"):
                st.session_state[f"{key}_expanded"] = False
                st.rerun(scope="fragment")
        else:
            st.caption(":small["+ text[:max_chars] + "... ]")
            if st.button("Show more", key=f"{key}_expand", type="tertiary"):
                st.session_state[f"{key}_expanded"] = True
                st.rerun(scope="fragment")

def button_with_description(label, description):
    """Creates a button with a main label and long description inside it."""

    st.markdown(
        """
        <style>
            div.stButton > button {
                text-align: left;
                white-space: normal;
                line-height: 1.2;
                padding-top: 0.55rem;
                padding-bottom: 0.55rem;
            }
            div.stButton > button p {
                margin: 0;
                text-align: left;
            }
            div.stButton > button p + p {
                font-size: 0.82em;
                opacity: 0.82;
                margin-top: 0.12rem;
            }
            
        </style>
        """,
        unsafe_allow_html=True,
    )

    content = f"{label}\n\n :small {description}"

    return st.button(content, width="stretch")
