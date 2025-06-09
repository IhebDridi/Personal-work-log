import streamlit as st
from datetime import datetime
from shift_management.settings import set_user_settings
from shift_management.db import remove_user_fully

def run(username, settings):
    st.subheader("Account settings")
    col1, col2 = st.columns(2)
    with col1:
        # Parse defaults to time objects:
        try:
            def_start_time = datetime.strptime(settings['default_start'], "%H:%M").time()
        except Exception:
            def_start_time = datetime.strptime("09:00", "%H:%M").time()
        try:
            def_end_time = datetime.strptime(settings['default_end'], "%H:%M").time()
        except Exception:
            def_end_time = datetime.strptime("17:00", "%H:%M").time()

        default_start = st.time_input("Default start time", def_start_time)
        default_end = st.time_input("Default end time", def_end_time)
        time_mode = st.radio("Time display mode", ("24h", "12h"), index=0 if settings['time_mode']=="24h" else 1)
    with col2:
        vacation_days = st.number_input("Total vacation days per year", min_value=0, step=1, value=int(settings['vacation_days']))

    if st.button("Save settings"):
        set_user_settings(
            username,
            default_start.strftime("%H:%M"),
            default_end.strftime("%H:%M"),
            time_mode,
            vacation_days
        )
        st.success("Settings updated.")
     # --- Account Deletion Section ---
    st.markdown("---")
    st.markdown("### Danger zone: Account removal")
    if st.button("Delete my account and all data", type="primary"):
        if st.checkbox("Yes, I really want to delete my account and all my data.", key="confirm_delete"):
            remove_user_fully(username)
            st.success("Your user, settings, and all shift data were deleted. App will now log you out.")
            st.session_state.username = ""
            st.rerun()
        else:
            st.warning("You must tick the box to confirm account removal.")