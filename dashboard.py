import streamlit as st
import json
import os
from cryptography.fernet import Fernet


DATA_FILE = "stored_data.json"
KEY_FILE = "secret.key"


def load_key():
    if os.path.exists(KEY_FILE):
        return open(KEY_FILE, "rb").read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

fernet = Fernet(load_key())


def show_store_data():
    st.subheader("🔐 Store Data")
    data = st.text_area("Enter your data here")
    password = st.text_input("Enter a password", type="password")
    if st.button("Encrypt and Store"):
        encrypted_data = fernet.encrypt(data.encode()).decode()
        record = {"data": encrypted_data, "password": password}
        
        
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                all_data = json.load(f)
        else:
            all_data = []

        all_data.append(record)

        
        with open(DATA_FILE, "w") as f:
            json.dump(all_data, f)

        st.success("✅ Data encrypted and stored successfully!")


def show_retrieve_data():
    st.subheader("🔓 Retrieve Data")
    secret_key = st.text_input("Paste your encrypted data (copied from view):")
    password = st.text_input("Enter your password", type="password")
    if st.button("Decrypt Data"):
        try:
            
            decrypted_data = fernet.decrypt(secret_key.encode()).decode()
            
            
            with open(DATA_FILE, "r") as f:
                all_data = json.load(f)
                
            found = False
            for record in all_data:
                if record["data"] == secret_key and record["password"] == password:
                    st.success(f"✅ Your decrypted data:\n\n{decrypted_data}")
                    found = True
                    break
            if not found:
                st.error("❌ Password does not match this data.")
        except Exception as e:
            st.error("⚠️ Invalid secret key.")


def show_all_data():
    st.subheader("📂 View All Stored Data")
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            all_data = json.load(f)

        for i, record in enumerate(all_data):
            encrypted_data = record["data"]
            st.code(encrypted_data, language='text')  
            st.caption(f"Password protected record #{i + 1}")
            
            
            copy_button = st.button(f"Copy Secret Key for record #{i + 1}")
            if copy_button:
                st.write("📋 Secret Key copied to clipboard!")
                
                st.text_area("Encrypted Data (copied)", value=encrypted_data, height=0, max_chars=10000)
    else:
        st.info("ℹ️ No data stored yet.")
