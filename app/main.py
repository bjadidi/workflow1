import streamlit as st
from app.pages import input_page, output_page

st.set_page_config(layout="wide")
st.markdown("""<style>.css-18ni7ap.e8zbici2 { display: none !important; }</style>""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Input"

if st.session_state.page == "Input":
    input_page.show()
else:
    output_page.show()