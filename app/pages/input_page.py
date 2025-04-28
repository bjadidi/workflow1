import streamlit as st

def show():
    st.markdown("""
    <style>
        :root {
            --primary-color: #6BCB77;  /* Original green */
            font-size: 18px;           /* Base font size */
        }
        
        /* Global font size */
        .stApp, .stMarkdown, p, div, span {
            font-size: 20px !important;
        }
        
        /* Except for the about text which should be larger */
        .large-text {
            font-size: 25px !important;
            line-height: 1.6 !important;
        }
        
        /* Page title */
        h1 {
            font-size: 2.5rem !important;
            font-weight: 600 !important;
            margin-bottom: 2rem !important;
            text-align: center;
        }
        
        /* Section title */
        .section-title {
            font-size: 1.6rem !important;
            font-weight: 600 !important;
            color: white;
            margin-bottom: 1.5rem;
            padding-bottom: 0.8rem;
            border-bottom: 1px solid var(--primary-color);
        }
        
        /* Form labels */
        .stSlider label p, .stCheckbox label p {
            font-size: 1.2rem !important;
            font-weight: 500 !important;
        }
        
        /* Certification label */
        .cert-label {
            font-weight: 500;
            font-size: 1.2rem !important;
            margin-bottom: 0.5rem;
        }
        
        /* Make slider taller */
        .stSlider [data-baseweb="slider"] {
            height: 1.2rem !important;
        }
        
        /* Button styling */
        .stButton>button {
            font-size: 1.3rem !important;
            font-weight: 500 !important;
            padding: 0.7rem 2rem !important;
            background-color: var(--primary-color) !important;
            border: none !important;
            border-radius: 6px !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton>button:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
            filter: brightness(1.05) !important;
        }
        
        /* Add some spacing between sections */
        .section-spacing {
            margin-top: 3rem;
            margin-bottom: 1rem;
        }
        
        /* Right-aligned container */
        .right-align {
            display: flex;
            justify-content: flex-end;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Biopolymer Selection & Insights Tool")

    filters = st.session_state.get("filters", {})

    # About This Tool with larger text - trying a new approach
    st.markdown('<div class="section-title">About This Tool</div>', unsafe_allow_html=True)
    
    # Using a raw HTML approach with explicit styling
    about_text = """
    This tool is designed to guide you in identifying the most suitable base 
    biopolymer grades for mono-layer, high barrier flexible films for Europe and 
    Asia markets. It also provides targeted insights on how to address any performance 
    gaps by recommending complementary polymers, ingredients, and processing techniques. 
    Our goal is to support your hypothesis development and DOE process. You'll have the 
    opportunity to share feedback on the next screen—we'd love to hear your thoughts.
    """
    
    # Use st.write with raw HTML for full control
    st.markdown(f'<div style="font: 40px !important; line-height: 1.6;">{about_text}</div>', unsafe_allow_html=True)

    # Performance Requirements
    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Performance Requirements</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        tensile = st.slider("Tensile Strength (MPa)", 0, 200, filters.get("tensile", (20, 100)), key="tensile")
        # skip tow lines
        st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
        wvtr = st.slider("WVTR (g/m²·day)", 0.0, 40.0, filters.get("wvtr", (1.0, 10.0)), key="wvtr")
    with col2:
        elongation = st.slider("Elongation at Break (%)", 0, 1000, filters.get("elongation", (100, 600)), key="elongation")
        # otr = st.slider("OTR (cc/m²·day)", 0.0, 100.0, filters.get("otr", (5.0, 50.0)), key="otr")

    # Cost Criteria
    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Cost Criteria</div>', unsafe_allow_html=True)
    cost = st.slider("Estimated Cost (USD/kg)", 0.0, 20.0, filters.get("cost", (1.0, 10.0)), key="cost")

    # Sustainability Attributes
    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sustainability Attributes</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        bbc = st.slider("Biobased Content (BC %)", 0, 100, filters.get("bbc", (0, 100)), key="bbc")
    with col2:
        st.markdown('<div class="cert-label">Certifications:</div>', unsafe_allow_html=True)
        certs = []
        for cert in ["TUV Home", "TUV Industrial", "BPI"]:
            if st.checkbox(cert, value=cert in filters.get("certs", []), key=f"cert_{cert}"):
                certs.append(cert)

    # Set the static value for geos
    geos = "Asia"

    # Store selections in session state
    st.session_state.filters = {
        "tensile": tensile,
        "elongation": elongation,
        "wvtr": wvtr,
        "cost": cost,
        "bbc": bbc,
        "certs": certs,
        "geos": geos
    }

    # Button in bottom right using columns approach
    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
    cols = st.columns([3, 1])
    with cols[1]:  # Right column
        if st.button("Show me Polymers"):
            st.session_state.page = "Output"
            st.rerun()