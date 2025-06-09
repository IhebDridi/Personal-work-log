import streamlit as st
import bcrypt

from shift_management.db import (
    init_db, register_user, user_exists, get_password_hash
)
from shift_management.settings import get_user_settings

from views import account_status, add_shift, past_shifts, account_settings




# ---------- App Startup ----------
init_db()
st.title("Work Hours Logger (SQLite)")

# ---------- Authentication UI and Logic ----------
if "username" not in st.session_state:
    st.session_state.username = ""


# --- Privacy Policy Modal Toggle ---
if "show_privacy" not in st.session_state:
    st.session_state.show_privacy = False

if not st.session_state.username:
    st.subheader("Welcome! Please Sign Up or Log In.")

    if st.button("Read privacy policy"):
        st.session_state.show_privacy = True

    if st.session_state.show_privacy:
        st.markdown("""
        ---
        ### 🔒 Privacy Notice for Work Hours Logger

        - **What we collect:**  
          Your username, work shift times, and vacation entries.
        - **How we store it:**  
          Data is securely stored in a Supabase cloud database accessible only via this app’s code. Passwords are hashed using strong industry standards.
        - **Who can see your data:**  
          Only you (as the logged-in user) can view and edit your own shifts. Other users cannot access your data, and you cannot access theirs.
        - **Why we collect it:**  
          To help you track, analyze, and manage your work/vacation records for your own benefit.
        - **Where is your data stored:**  
          On the Supabase cloud platform, which may host data within or outside the EU.
        - **How long:**  
          Until you choose to delete your account, or until the project is shut down.

        **Your rights:**
        - You can view, download, or export your recorded data at any time.
        - **You can delete your account and erase all your data at any time via the 'Account settings' page in the app.**
        - You can also contact the admin at `iheb.dridi@stud.uni-due.de` for further assistance or data removal.
        - We will never share your data with third parties.

        By signing up or logging in, you consent to store and process your data in accordance with this notice and the [Supabase privacy policy](https://supabase.com/privacy).

        ---
        """)
        if st.button("Close privacy policy"):
            st.session_state.show_privacy = False
        st.stop()  # Only show privacy until closed

    choice = st.radio("Choose an option", ["Login", "Sign Up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

# Checkbox for privacy policy consent, required for Sign Up
    consent = True  # always True for login
    if choice == "Sign Up":
        consent = st.checkbox("I have read and agree to the Privacy Policy above.", value=False)

    if choice == "Sign Up":
        if st.button("Sign Up"):
            if not username.strip() or not password.strip():
                st.warning("Please enter both a username and a password.")
            elif not consent:
                st.warning("You must agree to the privacy policy to sign up.")
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