import streamlit as st
import pandas as pd
from datetime import datetime

from .logic import fmt_time

def shifts_table(df, mode):
    df_show = df.copy()
    df_show["Start"] = df_show["Start"].apply(lambda x: fmt_time(x, mode))
    df_show["Actual End"] = df_show["Actual End"].apply(lambda x: fmt_time(x, mode))
    if "Scheduled End" in df_show.columns:
        df_show["Scheduled End"] = df_show["Scheduled End"].apply(lambda x: fmt_time(x, mode))
    if "Vacation" in df_show.columns:
        df_show["Vacation"] = df_show["Vacation"].apply(lambda x: "Yes" if int(x) == 1 else "No")
    if "Unpaid Vacation" in df_show.columns:
        df_show["Unpaid Vacation"] = df_show["Unpaid Vacation"].apply(lambda x: "Yes" if int(x) == 1 else "No")
    # Drop columns for past shift summary if present
    if "Scheduled End" in df_show.columns and "Vacation" in df_show.columns and "Unpaid Vacation" in df_show.columns:
        df_show_display = df_show.drop(columns=["Scheduled End", "Vacation", "Unpaid Vacation"])
    else:
        df_show_display = df_show
    st.dataframe(df_show_display, use_container_width=True)

def edit_shift_form(df, on_update):
    st.subheader("Edit a shift")
    shift_ids = df["ID"].tolist()
    if len(shift_ids) > 0:
        def format_shift_date(id):
            date_val = df[df["ID"] == id]["Date"].iloc[0]
            if hasattr(date_val, "strftime"):
                return date_val.strftime("%Y-%m-%d")
            try:
                return pd.to_datetime(date_val).strftime("%Y-%m-%d")
            except Exception:
                if isinstance(date_val, str):
                    if "T" in date_val:
                        return date_val.split("T")[0]
                    elif "-" in date_val:
                        return date_val[:10]
                return str(date_val)
        selected_id = st.selectbox(
            "Choose a shift to edit (by date)",
            shift_ids,
            format_func=format_shift_date
        )
        row = df[df["ID"] == selected_id].iloc[0]
        # Date parsing
        date_val = row["Date"]
        if isinstance(date_val, pd.Timestamp):
            edit_date = st.date_input("Edit Date", date_val.date(), key=f"edit_date_{selected_id}")
        elif isinstance(date_val, datetime):
            edit_date = st.date_input("Edit Date", date_val.date(), key=f"edit_date_{selected_id}")
        elif isinstance(date_val, str) and "-" in date_val:
            try:
                edit_date = st.date_input("Edit Date", datetime.strptime(date_val[:10], "%Y-%m-%d").date(), key=f"edit_date_{selected_id}")
            except Exception:
                edit_date = st.date_input("Edit Date", datetime.today().date(), key=f"edit_date_{selected_id}")
        else:
            edit_date = st.date_input("Edit Date", datetime.today().date(), key=f"edit_date_{selected_id}")
        # --- TIME INPUTS
        def parse_time_field(val):
            if isinstance(val, str) and ":" in val:
                try:
                    return datetime.strptime(val, "%H:%M").time()
                except Exception:
                    return datetime.now().time()
            elif isinstance(val, datetime):
                return val.time()
            else:
                return datetime.now().time()
        edit_start = st.time_input("Edit Start time", parse_time_field(row["Start"]), key=f"edit_start_{selected_id}")
        edit_sched_end = st.time_input("Edit Scheduled End time", parse_time_field(row["Scheduled End"]), key=f"edit_sched_{selected_id}")
        edit_actual_end = st.time_input("Edit Actual End time", parse_time_field(row["Actual End"]), key=f"edit_actual_{selected_id}")
        edit_is_vac = st.checkbox("Vacation day", bool(int(row["Vacation"])), key=f"edit_vacation_{selected_id}")
        edit_is_unpaid_vac = st.checkbox("Unpaid Vacation day", bool(int(row["Unpaid Vacation"])), key=f"edit_unpaid_vac_{selected_id}")
        # Enforce mutually exclusive vacation options
        if edit_is_vac and edit_is_unpaid_vac:
            st.warning("Please select only one vacation option (paid or unpaid).")
        if st.button("Update shift", key=f"update_{selected_id}"):
            on_update(
                selected_id,
                edit_date,
                edit_start.strftime("%H:%M"),
                edit_sched_end.strftime("%H:%M"),
                edit_actual_end.strftime("%H:%M"),
                edit_is_vac,
                edit_is_unpaid_vac
            )