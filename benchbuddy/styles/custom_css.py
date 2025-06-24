# Deze code zorgt ervoor dat de streamlit applicatie een eigen stijl krijgt.
# Dit wordt gedaan m.b.v. CSS-stijlen.

# Met ChatGPT is een CSS code gemaakt:

# Knoppen: groene, witte tekst en dikke letters.
# Titels: dikke letters, groene kleur.
# Sectiekoppen: Dikke letters, donker groene kleur.
# Sidebar: Lichtgrijse achtergrond.


import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        .stButton > button {
            background-color: #28a745 !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }
        .title {
            font-size: 2.5em;
            font-weight: 700;
            color: #28a745;
            margin-bottom: 10px;
        }
        .section-header {
            font-size: 1.8em;
            font-weight: 600;
            color: #117a37;
            margin-bottom: 15px;
        }
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #d9f2d9 !important;
        }
    </style>
    """, unsafe_allow_html=True)
