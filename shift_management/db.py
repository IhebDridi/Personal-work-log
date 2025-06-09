from supabase import create_client, Client
import streamlit as st

# Initialize Supabase client using Streamlit Secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- USER AUTH ----------

def register_user(username, password_hash):
    try:
        result = supabase.table("users").insert({"username": username, "password_hash": password_hash}).execute()
        return not result.get("error")
    except Exception as e:
        return False

def user_exists(username):
    try:
        result = supabase.table("users").select("username").eq("username", username).execute()
        return result.data is not None and len(result.data) > 0
    except Exception as e:
        return False

def get_password_hash(username):
    try:
        result = supabase.table("users").select("password_hash").eq("username", username).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]["password_hash"]
    except Exception:
        pass
    return None

def remove_user_fully(username):
    try:
        supabase.table("users").delete().eq("username", username).execute()
        supabase.table("shifts").delete().eq("username", username).execute()
        supabase.table("user_settings").delete().eq("username", username).execute()
    except Exception:
        pass

# ---------- SHIFTS MANAGEMENT ----------

def save_shift(username, date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation, is_unpaid_vacation):
    try:
        supabase.table("shifts").insert({
            "username": username,
            "date": date,
            "start": start,
            "scheduled_end": scheduled_end,
            "actual_end": actual_end,
            "hours_worked": hours_worked,
            "overtime": overtime,
            "is_vacation": is_vacation,
            "is_unpaid_vacation": is_unpaid_vacation
        }).execute()
    except Exception:
        pass

def update_shift(shift_id, date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation, is_unpaid_vacation):
    try:
        supabase.table("shifts").update({
            "date": date,
            "start": start,
            "scheduled_end": scheduled_end,
            "actual_end": actual_end,
            "hours_worked": hours_worked,
            "overtime": overtime,
            "is_vacation": is_vacation,
            "is_unpaid_vacation": is_unpaid_vacation
        }).eq("id", shift_id).execute()
    except Exception:
        pass

def get_user_shifts(username):
    try:
        result = supabase.table("shifts") \
            .select("*") \
            .eq("username", username) \
            .order("date", desc=True) \
            .execute()
        return [
            (
                shift["id"],
                shift["date"],
                shift["start"],
                shift["scheduled_end"],
                shift["actual_end"],
                shift["hours_worked"],
                shift["overtime"],
                shift["is_vacation"],
                shift["is_unpaid_vacation"],
            )
            for shift in result.data
        ] if result and result.data else []
    except Exception:
        return []

def get_shift_by_id(shift_id):
    try:
        result = supabase.table("shifts").select("*").eq("id", shift_id).execute()
        if result.data and len(result.data) > 0:
            shift = result.data[0]
            return (
                shift["id"],
                shift["date"],
                shift["start"],
                shift["scheduled_end"],
                shift["actual_end"],
                shift["hours_worked"],
                shift["overtime"],
                shift["is_vacation"],
                shift["is_unpaid_vacation"],
            )
    except Exception:
        pass
    return None

# ---------- USER SETTINGS ----------

def get_user_settings(username):
    try:
        result = supabase.table("user_settings").select("*").eq("username", username).execute()
        if result.data and len(result.data) > 0:
            row = result.data[0]
            return {
                "default_start": row.get("default_start", "09:00"),
                "default_end": row.get("default_end", "17:00"),
                "time_mode": row.get("time_mode", "24h"),
                "vacation_days": row.get("vacation_days", 20),
            }
    except Exception:
        pass
    return None

def set_user_settings(username, default_start, default_end, time_mode, vacation_days):
    try:
        supabase.table("user_settings").upsert({
            "username": username,
            "default_start": default_start,
            "default_end": default_end,
            "time_mode": time_mode,
            "vacation_days": vacation_days
        }).execute()
    except Exception:
        pass
