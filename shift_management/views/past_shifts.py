import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
from shift_management.db import get_user_shifts, update_shift
from shift_management.logic import calc_ot
from shift_management.ui import shifts_table, edit_shift_form

def run(username, settings):
    shifts = get_user_shifts(username)
    if len(shifts) == 0:
        st.info("No past shifts yet. Add your first shift!")
        return
    columns = ["ID", "Date", "Start", "Scheduled End", "Actual End",
               "Worked (h)", "Overtime (h)", "Vacation", "Unpaid Vacation"]
    df = pd.DataFrame(shifts, columns=columns)
    df_show = df.copy()
    # Format columns if needed (see previous logic...)
    # Hide ID, Scheduled End, Vacation, Unpaid Vacation
    df_show_display = df_show.drop(columns=["ID", "Scheduled End", "Vacation", "Unpaid Vacation"])
    st.subheader("Past Shifts")
    st.dataframe(df_show_display, use_container_width=True)
    
    # ---- Monthly summary table ----
    # Get the current year and month
    now = datetime.now()
    this_month = now.month
    this_year = now.year
    month_name = calendar.month_name[this_month]

    # Ensure Date column is parsed as date
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter rows matching current month, not vacation nor unpaid vacation
    mask = (
        (df['Date'].dt.month == this_month) & 
        (df['Date'].dt.year == this_year) &
        (df["Vacation"] == 0) & 
        (df["Unpaid Vacation"] == 0)
    )
    df_month = df.loc[mask]

    # Calculate summary values
    total_worked_days = len(df_month)
    total_worked_hours = df_month["Worked (h)"].sum()
    total_overtime_hours = df_month["Overtime (h)"].sum()

    summary_df = pd.DataFrame([{
        "Month": month_name,
        "Worked Days": total_worked_days,
        "Worked Hours": round(total_worked_hours, 2),
        "Overtime Hours": round(total_overtime_hours, 2)
    }])

    # Display summary table under main table
    st.markdown("#### This Month's Summary")
    st.table(summary_df)

    def on_update(shift_id, new_date, new_start, new_sched_end, new_actual_end, new_is_vac, new_is_unpaid_vac):
        if new_is_vac and new_is_unpaid_vac:
            st.warning("Can't be both paid and unpaid vacation!")
            return
        try:
            if new_is_unpaid_vac:
                hours_worked, overtime = -8, 0
            elif new_is_vac:
                hours_worked, overtime = 0, 0
            else:
                hours_worked, overtime = calc_ot(new_start, new_sched_end, new_actual_end)
            update_shift(
                shift_id,
                new_date.strftime("%Y-%m-%d"),
                new_start, new_sched_end, new_actual_end,
                hours_worked, overtime, int(new_is_vac), int(new_is_unpaid_vac)
            )
            st.success("Updated shift.")
            st.experimental_rerun()
        except Exception as ex:
            st.error(f"Error updating: {ex}")

    edit_shift_form(df, on_update)