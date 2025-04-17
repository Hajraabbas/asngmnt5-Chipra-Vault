import streamlit as st
import json
import os
from cryptography.fernet import Fernet

USER_DB = "users.json"
KEY_FILE = "secret.key"


def load_key():
    if os.path.exists(KEY_FILE):
        return open(KEY_FILE, "rb").read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

fernet = Fernet(load_key())


def is_authenticated():
    return st.session_state.get("is_logged_in", False)


def login_register_page():
    st.markdown("<h2 style='text-align:center;'>🔐 Ciphra Vault Login</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔑 Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            login_user(username, password)

    with col2:
        st.subheader("📝 Register")
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register"):
            register_user(new_user, new_pass)

def register_user(user, pwd):
    users = {}
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            users = json.load(f)

    if user in users:
        st.error("⚠️ Username already exists!")
    else:
        users[user] = fernet.encrypt(pwd.encode()).decode()
        with open(USER_DB, "w") as f:
            json.dump(users, f)
        st.success("✅ Registered! Please login.")

def login_user(user, pwd):
    st.session_state.failed_attempts = st.session_state.get("failed_attempts", 0)

    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            users = json.load(f)

        if user in users:
            decrypted = fernet.decrypt(users[user].encode()).decode()
            if decrypted == pwd:
                st.session_state["is_logged_in"] = True
                st.session_state["username"] = user
                st.session_state.failed_attempts = 0
                st.success("✅ Login Successful!")
            else:
                st.session_state.failed_attempts += 1
                st.error("❌ Wrong password!")
                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts. Logging out.")
                    logout_user()
        else:
            st.error("⚠️ User not found.")
    else:
        st.error("❗ No users registered yet.")

def logout_user():
    st.session_state.clear()
    st.rerun()
