import streamlit as st

# --- Replace this with secure handling in production ---
USERS = {
    "Nima": "nima123",
    "Jill": "jill123",
    "Bruce": "bruce123",
    "Kritika": "kritika123",
    "Audren": "audren123"
}

def login():

    st.session_state.user = "Admin"
    st.session_state.page = "Input"
    # st.rerun()


    # st.title("🔐 Login")
    # username = st.text_input("Username")
    # password = st.text_input("Password", type="password")

    # if st.button("Login"):
    #     if username in USERS and USERS[username] == password:
    #         st.session_state.user = username
    #         st.session_state.page = "Input"
    #         st.rerun()
    #     else:
    #         st.error("Invalid username or password. Please try again.")
