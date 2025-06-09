import streamlit as st
import bcrypt

from shift_management.db import (
    init_db, register_user, user_exists, get_password_hash,
    get_user_settings
)

from views import (
    account_status,
    add_shift,
    past_shifts,
    account_settings
)

# ---------- App Startup ----------
init_db()
st.title("Work Hours Logger (SQLite)")

# ---------- Authentication UI and Logic ----------
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    st.subheader("Welcome! Please Sign Up or Log In.")
    st.info(
        """
        **How to use the Work Hours Logger:**
        - Sign Up with a unique username and password, or log in if you already have an account.
        - Your data is protected: you can only see and edit your own shifts and settings.
        - Use the sidebar for: Account Status (stats & charts), Add Shift (log your work), Past Shifts (view/edit), and Account Settings (change your defaults).
        - All data is securely stored and instantly available after login.
        """
    )
    choice = st.radio("Choose an option", ["Login", "Sign Up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.button("Sign Up"):
            if not username.strip() or not password.strip():
                st.warning("Please enter both a username and a password.")
            elif user_exists(username.strip()):
                st.error("That username already exists. Please choose another.")
            else:
                password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                if register_user(username.strip(), password_hash):
                    st.success("Registration successful! Please log in.")
                else:
                    st.error("Registration failed. Please try again.")
    else:  # Login
        if st.button("Login"):
            if not username.strip() or not password.strip():
                st.warning("Please enter your username and password.")
            else:
                stored_hash = get_password_hash(username.strip())
                if stored_hash and bcrypt.checkpw(password.encode(), stored_hash.encode()):
                    st.session_state.username = username.strip()
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
    st.stop()

username = st.session_state.username
settings = get_user_settings(username) or {
    'default_start': '09:00',
    'default_end': '17:00',
    'time_mode': '24h',
    'vacation_days': 20
}

# ---------- Sidebar Layout and Navigation ----------
choice = st.sidebar.radio("Menu", ("Account status", "Add shift", "Past shifts", "Account settings"))
if st.sidebar.button("Logout"):
    st.session_state.username = ""
    st.rerun()
st.sidebar.markdown(f"**Logged in as:** `{username}`")

# ---------- Main Content Navigation ----------
if choice == "Account status":
    account_status.run(username, settings)
elif choice == "Add shift":
    add_shift.run(username, settings)
elif choice == "Past shifts":
    past_shifts.run(username, settings)
elif choice == "Account settings":
    account_settings.run(username, settings)