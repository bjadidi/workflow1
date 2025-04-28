import streamlit as st
import pandas as pd
from llm_handler import call_llm 

# Load data
@st.cache_data
def load_data():
    file = "./Data_Rule_Based/Extended_Unified_Polymer_Model.xlsx"
    return pd.read_excel(file)

data = load_data()

# # Placeholder for LLM reference extraction function
# def call_llm(user_input, prompt, llm_model_name):
#     # This function would typically send user_input + prompt to an LLM model
#     # hosted externally or locally and return a parsed or synthesized answer.
#     return f"[LLM OUTPUT for prompt: '{prompt}' and input: '{user_input}']"

# Streamlit App UI
st.title("Polymer Blend Recommendation:do ")

# Inputs
base_polymer = st.selectbox("Select Base Polymer", sorted(data["Polymer A"].unique()))
category = st.selectbox("Select Optimization Category", sorted(data["Category"].unique()))

if st.button("Get Recommendations"):
    # Filter recommendations
    df = data[(data["Polymer A"] == base_polymer) & (data["Category"] == category)]
    if df.empty:
        st.warning("No matches found for this polymer and category.")
    else:
        st.subheader("Recommended Blends")
        for _, row in df.iterrows():
            st.markdown(f"### Blend: {row['Polymer A']} + {row['Polymer B']}")
            st.write(f"**Mechanism:** {row['Mechanism']}")
            st.write(f"**Effect:** {row['Effect']}")
            st.write(f"**Compatibility:** {row['Compatibility Type']}")
            st.write(f"**Recommended wt%:** {row['Recommended wt%']}, Max Processing: {row['Max Processing']}, Max Compostability: {row['Max Compostability']}")
            st.write(f"**Reference:** {row['Reference']}")
            
            # Optional: Ask LLM to extract insights from the reference
            explanation = call_llm(
                user_input=f"Explain why {row['Polymer B']} is a good match for {row['Polymer A']} in the context of {row['Category']}.",
                prompt=f"Use this reference: {row['Reference']} and summarize the mechanism.",
                llm_model_name="gpt-4"
            )
            st.markdown(f"**LLM Insight:** {explanation}")
