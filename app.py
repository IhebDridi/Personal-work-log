import streamlit as st
from shift_management.db import init_db
from shift_management.settings import get_user_settings
from shift_management.views import (
    account_status,
    add_shift,
    past_shifts,
    account_settings
)

init_db()
st.title("Work Hours Logger (SQLite)")

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    st.subheader("Login")
    username = st.text_input("Username")
    if st.button("Login"):
        if username.strip():
            st.session_state.username = username.strip()
            st.rerun()
        else:
            st.warning("Please enter a username.")
    st.stop()

username = st.session_state.username
settings = get_user_settings(username) or {
    'default_start': '09:00',
    'default_end': '17:00',
    'time_mode': '24h',
    'vacation_days': 20
}

choice = st.sidebar.radio("Menu", ("Account status", "Add shift", "Past shifts", "Account settings"))
if st.sidebar.button("Logout"):
    st.session_state.username = ""
    st.rerun()
st.sidebar.markdown(f"**Logged in as:** `{username}`")

if choice == "Account status":
    account_status.run(username, settings)
elif choice == "Add shift":
    add_shift.run(username, settings)
elif choice == "Past shifts":
    past_shifts.run(username, settings)
elif choice == "Account settings":
    account_settings.run(username, settings)