from datetime import datetime

def calc_ot(start, sched_end, actual_end):
    t0 = datetime.strptime(start, "%H:%M")
    t1 = datetime.strptime(sched_end, "%H:%M")
    t2 = datetime.strptime(actual_end, "%H:%M")
    overtime = max(0, (t2-t1).total_seconds()/3600)
    total_time = (t2-t0).total_seconds()/3600
    return total_time, overtime

def fmt_time(t, mode):
    try:
        dt = datetime.strptime(t, "%H:%M")
        return dt.strftime("%I:%M %p") if mode == "12h" else dt.strftime("%H:%M")
    except Exception:
        return t  # fallback

def calc_account_stats(shifts, vacation_days_in_settings):
    shifts_df = [s for s in shifts if not s[-1]]  # not vacation
    vacation_shifts = [s for s in shifts if s[-1]]
    n_shifts = len(shifts_df)
    total_overtime = sum(s[6] for s in shifts_df if s[6] is not None)
    total_normal = sum(s[5] for s in shifts_df if s[5] is not None) - total_overtime
    vacations_used = len(vacation_shifts)
    vacation_days_left = vacation_days_in_settings - vacations_used
    return n_shifts, total_overtime, total_normal, vacation_days_left, vacations_used