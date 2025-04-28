import streamlit as st
import pandas as pd

st.title("📄 Excel Link Viewer")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        # Let user choose which column contains links
        link_column = st.selectbox("Select the column containing hyperlinks", df.columns)

        st.subheader("🔗 Clickable Links:")

        for idx, link in df[link_column].dropna().items():  # changed iteritems() to items()
            if isinstance(link, str) and link.startswith("http"):
                st.markdown(f"[{link}]({link})")
            else:
                st.markdown(f"❌ Invalid link at row {idx+2}")

    except Exception as e:
        st.error(f"❗ Error reading file: {e}")
