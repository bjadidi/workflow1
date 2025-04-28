
import streamlit as st
st.set_page_config(layout="wide")

from app.pages import input_page, output_page
from auth import login

# st.set_page_config(layout="wide")
st.markdown("""<style>.css-18ni7ap.e8zbici2 { display: none !important; }
[data-testid="stSidebar"] {display: none !important;} 
.css-1d391kg {padding: 2rem 5rem !important;} 
.css-ffhzg2 {transition: all 0.4s ease-in-out;} 
</style>""", unsafe_allow_html=True)

if "user" not in st.session_state:
    login.login()
elif "page" not in st.session_state:
    st.session_state.page = "Input"

if st.session_state.get("user") and st.session_state.page == "Input":
    input_page.show()
elif st.session_state.get("user"):
    output_page.show()