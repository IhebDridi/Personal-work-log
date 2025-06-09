import streamlit as st
from datetime import date, datetime
from shift_management.db import save_shift
from shift_management.logic import calc_ot

def run(username, settings):
    st.subheader("Add a Shift")
    today = date.today()
    col1, col2 = st.columns(2)
    with col1:
        shift_date = st.date_input("Date", today)
        default_start = datetime.strptime(settings['default_start'], "%H:%M").time()
        default_end = datetime.strptime(settings['default_end'], "%H:%M").time()
        start = st.time_input("Start time", default_start)
        scheduled_end = st.time_input("Scheduled end time", default_end)
        actual_end = st.time_input("Actual end time", default_end)
    with col2:
        is_vacation = st.checkbox("Is Paid Vacation", value=False)
        is_unpaid_vac = st.checkbox("Is Unpaid Vacation", value=False)
    if is_vacation and is_unpaid_vac:
        st.warning("Please select only one of paid or unpaid vacation.")
        st.stop()
    paid_or_unpaid_vac = is_vacation or is_unpaid_vac
    overtime = 0
    str_start = start.strftime("%H:%M")
    str_sched_end = scheduled_end.strftime("%H:%M")
    str_actual_end = actual_end.strftime("%H:%M")
    if paid_or_unpaid_vac:
        st.info("Vacation mode: Overtime and worked hours will be set automatically.")
        if is_unpaid_vac:
            st.info("Unpaid vacation: Worked time will be subtracted (-8h by default).")
            hours_worked = -8
        else:
            hours_worked = 0
    else:
        try:
            hours_worked, overtime = calc_ot(str_start, str_sched_end, str_actual_end)
        except Exception:
            hours_worked, overtime = 0, 0
    if st.button("Save shift"):
        if is_vacation and is_unpaid_vac:
            st.warning("Can't be both paid and unpaid vacation!")
        else:
            try:
                save_shift(
                    username,
                    shift_date.strftime("%Y-%m-%d"),
                    str_start, str_sched_end, str_actual_end,
                    hours_worked, overtime, int(is_vacation), int(is_unpaid_vac)
                )
                st.success("Shift saved.")
                st.rerun()
            except Exception as ex:
                st.error(f"Could not save shift: {ex}")