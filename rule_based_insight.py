import streamlit as st
import pandas as pd
from llm_handler import call_llm
import matplotlib.pyplot as plt

@st.cache_data
def load_polymer_blend_data():
    #file = "./Data_Rule_Based/Extended_Unified_Polymer_Model.xlsx"
    file = "./Data_Rule_Based/Biopolymer_Insight_Template_Filled.xlsx"

    return pd.read_excel(file)

from plotly.subplots import make_subplots
import plotly.graph_objects as go

PLOT_SCALE = 1
EXCEL_PATH = "./data/Bio_Dis_Data.xlsx"

def read_sheet_data(xls, sheet_name):
    df = pd.read_excel(xls, sheet_name=sheet_name, header=1)
    df = df.rename(columns={df.columns[0]: "Time (day)", df.columns[1]: df.columns[1].strip()})
    df = df[["Time (day)", df.columns[1]]].copy()
    df["Time (day)"] = pd.to_numeric(df["Time (day)"], errors='coerce')
    df[df.columns[1]] = pd.to_numeric(df[df.columns[1]], errors='coerce')
    return df.dropna()

def plot_ingredient(xls, ingredient_name):
    bio_sheet = f"{ingredient_name}_Bio"
    dis_sheet = f"{ingredient_name}_Dis"

    try:
        df_bio = read_sheet_data(xls, bio_sheet)
        df_dis = read_sheet_data(xls, dis_sheet)
    except Exception as e:
        st.warning(f"📉 Data not available for **{ingredient_name}**.")
        return

    y_bio = df_bio.columns[1]
    y_dis = df_dis.columns[1]

    fig = make_subplots(
        rows=1, cols=2,
        horizontal_spacing=0.12
    )

    # Plot 1: Biodegradation
    fig.add_trace(go.Scatter(
        x=df_bio["Time (day)"],
        y=df_bio[y_bio],
        mode='lines+markers',
        name='Biodegradation',
        marker=dict(symbol='circle', size=6 * PLOT_SCALE, color='#1f77b4'),
        line=dict(width=2 * PLOT_SCALE, color='#1f77b4')
    ), row=1, col=1)

    # Plot 2: Disintegration
    fig.add_trace(go.Scatter(
        x=df_dis["Time (day)"],
        y=df_dis[y_dis],
        mode='lines+markers',
        name='Disintegration',
        marker=dict(symbol='square', size=6 * PLOT_SCALE, color='#ff7f0e'),
        line=dict(width=2 * PLOT_SCALE, color='#ff7f0e')
    ), row=1, col=2)

    # === Add custom subplot titles ===
    fig.add_annotation(
    text=f"<b>Biodegradation Profile</b>",
    x=0.21, y=1.18, xref="paper", yref="paper",
    showarrow=False, font=dict(size=20, color="#FFFFFF")
    )
    fig.add_annotation(
    text=f"<b>Disintegration Profile</b>",
    x=0.80, y=1.18, xref="paper", yref="paper",
    showarrow=False, font=dict(size=20, color="#FFFFFF")
    )
    # Layout & styling
    fig.update_layout(
        height=int(350 * PLOT_SCALE),
        width=int(900 * PLOT_SCALE),
        margin=dict(t=80, b=40, l=40, r=20),
        # title=dict(
        #     text=f"<b>📈 Degradation Analysis for {ingredient_name}</b>",
        #     x=0.5, xanchor='center',
        #     font=dict(size=16 * PLOT_SCALE)
        # ),
        font=dict(size=int(12 * PLOT_SCALE)),
        plot_bgcolor='white',
        showlegend=False
    )

    # Axis styling
    for col in [1, 2]:
        fig.update_xaxes(title_text="Time (days)", showgrid=True, gridcolor='lightgrey', zeroline=False, row=1, col=col)
    fig.update_yaxes(title_text=y_bio, showgrid=True, gridcolor='lightgrey', zeroline=False, row=1, col=1)
    fig.update_yaxes(title_text=y_dis, showgrid=True, gridcolor='lightgrey', zeroline=False, row=1, col=2)

    st.plotly_chart(fig, use_container_width=True)

# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# # === Adjustable Scaling Constant ===
# PLOT_SCALE = 1  # 0.5 (compact), 0.7 (nice), 1.0 (large)

# EXCEL_PATH = "./data/Bio_Dis_Data.xlsx"

# def read_sheet_data(xls, sheet_name):
#     df = pd.read_excel(xls, sheet_name=sheet_name, header=1)
#     df = df.rename(columns={df.columns[0]: "Time (day)", df.columns[1]: df.columns[1].strip()})
#     df = df[["Time (day)", df.columns[1]]].copy()
#     df["Time (day)"] = pd.to_numeric(df["Time (day)"], errors='coerce')
#     df[df.columns[1]] = pd.to_numeric(df[df.columns[1]], errors='coerce')
#     return df.dropna()

# def plot_ingredient(xls, ingredient_name):
#     bio_sheet = f"{ingredient_name}_Bio"
#     dis_sheet = f"{ingredient_name}_Dis"

#     try:
#         df_bio = read_sheet_data(xls, bio_sheet)
#         df_dis = read_sheet_data(xls, dis_sheet)
#     except Exception as e:
#         #st.warning(f"Skipping {ingredient_name}: {e}")
#         st.warning(f"Data is not available for {ingredient_name}")
#         return

#     y_bio = df_bio.columns[1]
#     y_dis = df_dis.columns[1]

#     fig = make_subplots(
#         rows=1, cols=2,
#         subplot_titles=("Degradation", "Disintegration"),
#         horizontal_spacing=0.12
#     )

#     # Plot 1: Degradation
#     fig.add_trace(go.Scatter(
#         x=df_bio["Time (day)"],
#         y=df_bio[y_bio],
#         mode='lines+markers',
#         name='Degradation',
#         marker=dict(symbol='circle', size=6 * PLOT_SCALE, color='#1f77b4'),
#         line=dict(width=2 * PLOT_SCALE, color='#1f77b4')
#     ), row=1, col=1)

#     # Plot 2: Disintegration
#     fig.add_trace(go.Scatter(
#         x=df_dis["Time (day)"],
#         y=df_dis[y_dis],
#         mode='lines+markers',
#         name='Disintegration',
#         marker=dict(symbol='square', size=6 * PLOT_SCALE, color='#ff7f0e'),
#         line=dict(width=2 * PLOT_SCALE, color='#ff7f0e')
#     ), row=1, col=2)

#     fig.update_layout(
#         height=int(300 * PLOT_SCALE),
#         width=int(800 * PLOT_SCALE),
#         margin=dict(t=40, b=40, l=40, r=20),
#         showlegend=False,
#         font=dict(size=int(12 * PLOT_SCALE)),
#         plot_bgcolor='white'
#     )

#     fig.update_xaxes(title_text="Time (day)", showgrid=True, gridcolor='lightgrey', zeroline=False, row=1, col=1)
#     fig.update_yaxes(title_text=y_bio, showgrid=True, gridcolor='lightgrey', zeroline=False, row=1, col=1)
#     fig.update_xaxes(title_text="Time (day)", showgrid=True, gridcolor='lightgrey', zeroline=False, row=1, col=2)
#     fig.update_yaxes(title_text=y_dis, showgrid=True, gridcolor='lightgrey', zeroline=False, row=1, col=2)

def show_polymer_blend_insights(polymer_name: str, key_prefix: str):
    import streamlit as st
    import pandas as pd

    # Load data
    data = load_polymer_blend_data()

    # Predefined category code → readable name
    category_mapping = {
        "MECH": "Mechanical",
        "THERM": "Thermal",
        "BARRIER": "Barrier",
        "COMPAT": "Compatibilization",
        "BIO": "Biodegradability",
        "PROC": "Processing",
        "COST": "Cost Optimization"
    }

    # --- User selects a category ---
    selected_display_name = st.selectbox(
        "Select Optimization Category",
        list(category_mapping.values()),
        key=f"{key_prefix}_category"
    )
    selected_code = next((code for code, name in category_mapping.items() if name == selected_display_name), None)

    # --- Filter the DataFrame ---
    filtered_df = data[
        (data["Base Polymer"].str.upper() == polymer_name.upper()) &
        (data["Category (Property)"].str.contains(selected_code, na=False))
    ].reset_index(drop=True)

    if filtered_df.empty:
        st.warning("⚠️ No blend insights found for this polymer and category.")
        return

    # --- Define fields to show ---
    display_cols = [
        "Ingredient", "Interaction Type", "Category (Property)", "Positive Effect", "Negative Effect",
        "Compatibility Type", "Recommended wt%", "Base Polymer Max wt%", "Max Processing Temp (°C)",
        "Max Compostability (%)", "Processing Notes", "Known Limitations", "Erthos Insight"
    ]

    # --- Create HTML rows for one row per additive ---
    html_header = "".join(
        f"<th style='padding: 10px; border: 1px solid #ddd; background-color: #8942E5; color: white;'>{col}</th>"
        for col in display_cols + ["Reference"]
    )

    html_rows = ""
    for _, row in filtered_df.iterrows():
        html_cells = ""
        for col in display_cols:
            val = row.get(col, "—") if pd.notna(row.get(col)) else "—"
            html_cells += f"<td style='padding: 10px; border: 1px solid #ddd;'>{val}</td>"

        ref = row.get("Reference", "").strip()
        link_html = f"<a href='{ref}' target='_blank' style='color:#4a90e2;'>View</a>" if ref else "—"
        html_cells += f"<td style='padding: 10px; border: 1px solid #ddd;'>{link_html}</td>"

        html_rows += f"<tr>{html_cells}</tr>"

    # --- Final styled table ---
    html_table = f"""
    <div style='margin-top: 20px; overflow-x: auto;'>
    <table style='width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 14px;'>
        <thead>
            <tr>
                {html_header}
            </tr>
        </thead>
        <tbody>
            {html_rows}
        </tbody>
    </table>
    </div>
    """

    # st.markdown("### 📊 Blend Recommendations (Styled Table)", unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)

    # --- Additive dropdown for LLM insight ---
    st.markdown("### 🔍 Deep Dive into a Specific Additive")
    selected_additive = st.selectbox("Choose an additive for insight", filtered_df["Ingredient"].tolist(), key=f"{key_prefix}_additive")
    selected_row = filtered_df[filtered_df["Ingredient"] == selected_additive].iloc[0]
    reference = selected_row.get("Reference", "").strip()

    # --- Trigger LLM insight ---
    if st.button("Generate LLM Insight", key=f"{key_prefix}_generate_llm"):
        if reference:
            prompt = (
                f"Based on the paper at {reference}, explain how blending {selected_row['Ingredient']} with {polymer_name} "
                f"enhances its {selected_display_name.lower()} properties. Mention mechanisms and experimental outcomes if relevant."
                f"If the paper is not relevant to the question, just Explain how blending {selected_row['Ingredient']} with {polymer_name} improves its {selected_display_name.lower()} properties."
                f"Discuss common mechanisms such as flexibility enhancement, crystallinity improvement, adhesion, or barrier performance."

            )
        else:
            prompt = (
                f"Explain how blending {selected_row['Ingredient']} with {polymer_name} improves its {selected_display_name.lower()} properties. "
                f"Discuss common mechanisms such as flexibility enhancement, crystallinity improvement, adhesion, or barrier performance."
            )

        explanation = call_llm(
            user_input=f"How does {selected_additive} improve {polymer_name} for {selected_display_name}?",
            prompt=prompt,
            llm_model_name="gpt-4"
        )
        st.markdown(f"""
        <div style='
            border: 2px solid #8942E5;              /* Border thickness & color */
            background-color: #f8f6ff;              /* Light background */
            border-radius: 8px;                     /* Rounded corners */
            padding: 16px;                          /* Inside spacing */
            margin-top: 20px;                       /* Space above */
            font-family: Arial, sans-serif;
            font-size: 15px;
            line-height: 1.6;
        '>
            <strong style='font-size: 16px;'>🤖 LLM Insight</strong><br><br>
            {explanation}
        </div>
        """, unsafe_allow_html=True)








# def show_polymer_blend_insights(polymer_category_name: str,key):
#     # st.markdown("---")
#     # st.subheader(f"🔍 Blend Recommendations for {polymer_category_name}")
#     data = load_polymer_blend_data()

#     category = st.selectbox("Select Optimization Category", sorted(data["Category"].unique()),key=key)

#     optimization_category = category
#     df = data[(data["Polymer A"] == polymer_category_name) & (data["Category"] == optimization_category)]

#     if df.empty:
#         st.warning("No matches found for this polymer and category.")
#         return

#     for _, row in df.iterrows():
#         st.markdown(f"### 🧪 Blend: {row['Polymer A']} + {row['Polymer B']}")
#         st.write(f"**Mechanism:** {row['Mechanism']}")
#         st.write(f"**Effect:** {row['Effect']}")
#         st.write(f"**Compatibility:** {row['Compatibility Type']}")
#         st.write(f"**Recommended wt% for {row['Polymer B']}:** {row['Recommended wt%']}")
#         st.write(f"**Recommended wt% for {row['Polymer A']}:** {row['Max Processing']}")
#         # st.write(f"Max Compostability: {row['Max Compostability']}")

#         st.write(f"**Reference:** {row['Reference']}")

#         if st.button("Show LLM insights",key=key+"button"):
#             explanation = call_llm(
#                 user_input=f"Explain why {row['Polymer B']} is a good match for {row['Polymer A']} in the context of {row['Category']}.",
#                 prompt=f"Use this reference: {row['Reference']} and summarize the mechanism.",
#                 llm_model_name="gpt-4"
#             )
#             st.markdown(f"**LLM Insight:** {explanation}")
