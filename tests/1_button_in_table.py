import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
st.set_page_config(layout="wide")

# --- Load Excel ---
excel_path = "../data/polymer_database_placeholder.xlsx"
df = pd.read_excel(excel_path)
df = df.reset_index(drop=True)

# Add Feedback & Details columns
df["Feedback"] = ""
df["Details"] = ""  # Placeholder for inline button

# --- Grid Config ---
gb = GridOptionsBuilder.from_dataframe(df)

# Configure columns
for col in df.columns:
    if col == "Feedback":
        gb.configure_column(col, editable=True, wrapText=True, autoHeight=True)
    elif col == "Details":
        gb.configure_column(
            col,
            header_name="Details",
            cellRenderer=JsCode("""
                class BtnCellRenderer {
                    init(params) {
                        this.params = params;
                        this.eGui = document.createElement('button');
                        this.eGui.innerText = 'Show';
                        this.eGui.className = 'btn btn-sm btn-primary';
                        this.eGui.addEventListener('click', () => {
                            alert(JSON.stringify(params.data, null, 2));
                        });
                    }
                    getGui() {
                        return this.eGui;
                    }
                }
            """),
            suppressSizeToFit=False,
            maxWidth=120
        )
    else:
        gb.configure_column(col, editable=False)

# --- Render AgGrid ---
st.markdown("## 🌌 Polymer Dataset with Embedded Feedback & Inline Details")

grid_options = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    fit_columns_on_grid_load=True,      # ✅ Auto-fit columns to screen
    allow_unsafe_jscode=True,
    enable_enterprise_modules=False,
    height=800,                         # ✅ Taller table view
    width='100%',                       # ✅ Full width
    theme="balham",                     # ✅ Dark-mode theme
)

# --- Optional Save Button ---
if st.button("💾 Export Feedbacks"):
    feedback_df = grid_response["data"][["Feedback"]]
    feedback_df.to_csv("feedbacks.csv", index=False)
    st.success("Feedbacks saved to feedbacks.csv!")
