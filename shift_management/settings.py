from shift_management.db import supabase

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