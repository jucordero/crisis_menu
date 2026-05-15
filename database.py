import streamlit as st
import gspread

@st.cache_data(ttl=3600)
def get_all_crisis_descriptions():
    """Fetch description data for all crisis from Google Sheets and cache it
    for 1 hour."""

    credentials = st.secrets["gspread"]["credentials"]
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_key(st.secrets["crisis_worksheet"])
    ws = sh.worksheet("Shock table")

    # First two rows are headers
    crisis_labels = ws.col_values(1)[2:]
    crisis_descriptions = ws.col_values(2)[2:]

    return crisis_labels, crisis_descriptions


@st.cache_data(ttl=3600)
def get_crisis_data(crisis_name):
    """Fetch data for specified crisis from Google Sheets and return it as a
    dictionary, caching the result for 1 hour."""

    credentials = st.secrets["gspread"]["credentials"]
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_key(st.secrets["crisis_worksheet"])
    ws = sh.worksheet("Shock table")

    # Find the row corresponding to the crisis name
    cell = ws.find(crisis_name)
    if cell is None:
        st.error(f"Crisis '{crisis_name}' not found in the database.")
        return None

    row = cell.row
    crisis_data = {
        "name": ws.cell(row, 1).value,
        "description": ws.cell(row, 2).value,
        "type": ws.cell(row, 3).value,
        "element": ws.cell(row, 4).value.split(", ") if ws.cell(row, 4).value else [],
        "items": ws.cell(row, 5).value.split(", ") if ws.cell(row, 5).value else [],
        "timescale": ws.cell(row, 6).value,
        "year": int(ws.cell(row, 7).value) if ws.cell(row, 7).value else None,
        "width": int(ws.cell(row, 8).value) if ws.cell(row, 8).value else None,
        "severity": int(ws.cell(row, 9).value) if ws.cell(row, 9).value else None,
        "region": ws.cell(row, 10).value,
    }

    return crisis_data

def write_crisis_to_database(crisis_data):
    """Write a new crisis to the Google Sheets database."""

    credentials = st.secrets["gspread"]["credentials"]
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_key(st.secrets["crisis_worksheet"])
    ws = sh.worksheet("Shock table")

    if crisis_data.get("width") is None:
        crisis_data["width"] = 0

    # Append the new crisis data as a new row
    new_row = [
        crisis_data.get("name", ""),
        crisis_data.get("description", ""),
        crisis_data.get("type", ""),
        ", ".join(crisis_data.get("element", [])),
        ", ".join(crisis_data.get("items", [])),
        crisis_data.get("timescale", ""),
        str(crisis_data.get("year", "")),
        str(crisis_data.get("width", "")),
        str(crisis_data.get("severity", "")),
        ", ".join(crisis_data.get("region", "")),
    ]
    ws.append_row(new_row)