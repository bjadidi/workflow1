import streamlit as st

html_table = """
<div style='overflow-x: auto; margin-top: 20px;'>
    <table style='width: 100%; border-collapse: collapse; font-family: Arial, sans-serif;'>
        <thead>
            <tr style='background-color: #2c3e50; color: white;'>
                <th style='padding: 8px; border: 1px solid #ccc;'>Property</th>
                <th style='padding: 8px; border: 1px solid #ccc;'>Value</th>
                <th style='padding: 8px; border: 1px solid #ccc;'>Reference</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style='padding: 8px; border: 1px solid #ccc;'>BPI</td>
                <td style='padding: 8px; border: 1px solid #ccc;'>Certified</td>
                <td style='padding: 8px; border: 1px solid #ccc;'>
                    <a href='https://products.bpiworld.org/?type=product&keyword=Natureworks' target='_blank'>View</a>
                </td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ccc;'>FDA or equivalent</td>
                <td style='padding: 8px; border: 1px solid #ccc;'>Approved</td>
                <td style='padding: 8px; border: 1px solid #ccc;'>
                    <a href='https://www.fda.gov' target='_blank'>View</a>
                </td>
            </tr>
        </tbody>
    </table>
</div>
"""

st.title("✅ HTML Table Rendering Test")
st.markdown(html_table, unsafe_allow_html=True)
