import streamlit as st
import pandas as pd

def display_polymer_info(df, category, grade):
    """
    Display polymer info in a custom-styled HTML table in Streamlit.
    Filters based on Polymer Category and Polymer Grade.
    Hides index and only shows non-empty fields.
    Includes a third column with links.
    """

    # Define relevant fields
    columns_to_show = [
        "Cost_Notes", "Volume Available", "TUV Home", "TUV Industrial", "BPI", 
        "BBC_Notes", "LCA (kg CO₂-eq)", "WVTR - Published Data", "WVTR_Conditions",
        "WVTR_Thickness (µm)", "WVTR_Standard", "WVTR_Notes", "Visual Appearance",
        "FDA or equivalent", "RoHS & REACH", "Europe Policy Considerations",
        "Asia Policy Considerations", "Production Methods", "CFE_Notes", "SC_Notes","Melt temperature (°C)"
    ]

    # Filter valid columns that exist
    valid_columns = [col for col in columns_to_show if col in df.columns]

    # Filter DataFrame
    filtered_df = df[
        (df["Polymer Category"] == category) &
        (df["Polymer Grade"] == grade)
    ]

    if filtered_df.empty:
        st.warning(f"No data found for category '{category}' and grade '{grade}'.")
        return

    # Extract first match and clean up empty values
    row = filtered_df.iloc[0][valid_columns]
    clean_row = row.dropna()
    clean_row = clean_row[clean_row.astype(str).str.strip() != ""]

    if clean_row.empty:
        st.info("No non-empty details available for the selected polymer.")
        return

    # Build HTML table manually with 3 columns
    html_rows = ""
    full_row = filtered_df.iloc[0]  # full row for access to *_Link fields


    # dictionary of links and column related
    link_columns = {
        "Cost_Notes": "Cost",
        "Volume Available": "Volume",
        "TUV Home": "TUV",
        "TUV Industrial": "TUV",
        "BPI": "BPI",
        "BBC_Notes": "BBC",
        "LCA (kg CO₂-eq)": "LCA_Link",
        "WVTR - Published Data": "WVTR_Link",
        "WVTR_Conditions": "WVTR",
        "WVTR_Thickness (µm)": "WVTR",
        "WVTR_Standard": "WVTR",
        "WVTR_Notes": "WVTR",
        "Visual Appearance": "Visual Appearance_Link",
        "FDA or equivalent": "FDA or equivalent_Link",
        "RoHS & REACH": "RoHS & REACH_Link",
        "Europe Policy Considerations": "Policy",
        "Asia Policy Considerations": "Policy",
        "Production Methods": "Production",
        "CFE_Notes": "CFE_Link",
        "SC_Notes": "SC_Link",
        "Melt temperature (°C)": "Melt temperature link"
    }

    for key, value in clean_row.items():
        #link_col = f"{key}_Link"
        link_col = link_columns[key]
        link = full_row[link_col] if link_col in full_row and pd.notna(full_row[link_col]) and str(full_row[link_col]).strip() else ""
        link_html = f"<a href='{link}' target='_blank'>View</a>" if link else "—"
        html_rows += f"<tr><td><strong>{key}</strong></td><td>{value}</td><td>{link_html}</td></tr>"

    html_table = f"""
    <div style='margin-top: 20px; overflow-x: auto;'>
    <table style='width: 100%; border-collapse: collapse; font-family: Arial, sans-serif;'>
        <thead>
            <tr style='background-color: #8942E5; color: white; text-align: left;'>
                <th style='padding: 8px; border: 1px solid #ccc;'>Property</th>
                <th style='padding: 8px; border: 1px solid #ccc;'>Value</th>
                <th style='padding: 8px; border: 1px solid #ccc;'>Reference</th>
            </tr>
        </thead>
        <tbody>
            {html_rows}
        </tbody>
    </table>
    </div>
    """

    st.markdown("### Additional details:", unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)
