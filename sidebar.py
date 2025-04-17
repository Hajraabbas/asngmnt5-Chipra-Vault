import streamlit as st
from auth import logout_user
from encryptor import encrypt_and_store, decrypt_data, show_data_list

def show_sidebar():
    st.sidebar.header("📂 Menu")
    option = st.sidebar.radio("Navigate", ["Home", "Store Data", "Retrieve Data", "View Stored Data", "Logout"])

    if option == "Store Data":
        encrypt_and_store()
    elif option == "Retrieve Data":
        decrypt_data()
    elif option == "View Stored Data":
        show_data_list()
    elif option == "Logout":
        logout_user()
