import streamlit as st

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

def authenticate(username, password):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def login():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")
    
    return st.session_state.authenticated
