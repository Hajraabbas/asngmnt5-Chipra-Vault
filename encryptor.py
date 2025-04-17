import streamlit as st
import json
import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"
DATA_FILE = "stored_data.json"

def load_key():
    return open(KEY_FILE, "rb").read()

fernet = Fernet(load_key())

def encrypt_and_store():
    st.subheader("🔒 Encrypt and Store Data")
    data = st.text_input("Enter data")
    passkey = st.text_input("Password to protect", type="password")
    if st.button("Store"):
        if data and passkey:
            encrypted = fernet.encrypt(data.encode()).decode()
            item = {"data": encrypted, "key": fernet.encrypt(passkey.encode()).decode()}
            save_data(item)
            st.success("✅ Data stored securely!")

def save_data(item):
    all_data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            all_data = json.load(f)
    all_data.append(item)
    with open(DATA_FILE, "w") as f:
        json.dump(all_data, f)

def decrypt_data():
    st.subheader("🔍 Retrieve Data")
    entered_key = st.text_input("Enter your password", type="password")
    if st.button("Retrieve"):
        all_data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                all_data = json.load(f)

        found = False
        for item in all_data:
            try:
                stored_pass = fernet.decrypt(item["key"].encode()).decode()
                if stored_pass == entered_key:
                    decrypted = fernet.decrypt(item["data"].encode()).decode()
                    st.success(f"🔓 Decrypted: {decrypted}")
                    found = True
                    break
            except:
                continue

        if not found:
            st.error("❌ Wrong password!")
            st.session_state.failed_attempts = st.session_state.get("failed_attempts", 0) + 1
            if st.session_state.failed_attempts >= 3:
                st.warning("🔒 Too many wrong attempts. Logging out.")
                from auth import logout_user
                logout_user()

def show_data_list():
    st.subheader("📁 All Stored Data (Encrypted)")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            all_data = json.load(f)
            for idx, item in enumerate(all_data):
                st.write(f"🔐 Data {idx + 1}: {item['data'][:20]}...")
