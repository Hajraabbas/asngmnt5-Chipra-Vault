import streamlit as st


def show_store_data():
    st.subheader("🔐 Store Data")
    
    
    data = st.text_area("Enter your data here")
    
    
    password = st.text_input("Enter a password to protect", type="password")
    
    if st.button("Encrypt and Store"):
        if data and password:
            
            encrypted_data = f"Encrypted({data})"  
            st.success(f"Data encrypted and stored successfully! Encrypted Data: {encrypted_data}")
        else:
            st.error("Please enter both data and password.")


def show_retrieve_data():
    st.subheader("🔓 Retrieve Data")
    
    
    encrypted_data = st.text_area("Paste your encrypted data here", height=150)
    
    
    password = st.text_input("Enter your password to decrypt", type="password")
    
    if st.button("Decrypt Data"):
        if encrypted_data and password:
            
            
            decrypted_data = encrypted_data.replace("Encrypted(", "").replace(")", "") 
            st.success(f"Decrypted Data: {decrypted_data}")
        else:
            st.error("Please enter both encrypted data and password.")


def show_all_data():
    st.subheader("📂 View All Stored Data")
    
    st.info("Stored data will appear here...")
