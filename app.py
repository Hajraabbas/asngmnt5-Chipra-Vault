import streamlit as st
from store_retrieve import show_store_data, show_retrieve_data, show_all_data
from auth import is_authenticated, login_register_page, logout_user
from sidebar import show_sidebar

def main():
    if is_authenticated():
        st.set_page_config(page_title="Chipra Vault", layout="wide")
        
        
        selected = show_sidebar()

        if selected == "Home":
            st.markdown("<h1 style='text-align: center;'>🚀 Welcome to Chipra Vault</h1>", unsafe_allow_html=True)
            st.image("logo.png", width=200)  

        # Store Data 
        elif selected == "Store Data":
            show_store_data()

        # Retrieve Data 
        elif selected == "Retrieve Data":
            show_retrieve_data()

        
        elif selected == "View Stored Data":
            show_all_data()

        
        elif selected == "Logout":
            logout_user()
    else:
        login_register_page()

if __name__ == "__main__":
    main()
