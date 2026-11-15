
import os
import sys
from io import BytesIO

import streamlit as st
from PIL import Image

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, BASE_DIR)

from src.pipeline import process_image

st.set_page_config(
    page_title="SmartBlur | AI Image Protection",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(35, 75, 120, 0.22),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #080d18 0%,
                #101827 50%,
                #080d18 100%
            );
        color: #f1f5f9;
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.035);
        border: 1px dashed rgba(96, 165, 250, 0.45);
        border-radius: 16px;
        padding: 20px;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #60a5fa;
    }

    .stButton > button {
        width: 100%;
        min-height: 52px;
        border: none;
        border-radius: 12px;
        background: linear-gradient(
            90deg,
            #2563eb,
            #0ea5e9
        );
        color: white;
        font-weight: 700;
        font-size: 16px;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3);
        color: white;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px;
        padding: 18px;
    }

    .section-label {
        color: #60a5fa;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(38px, 6vw, 66px);
        font-weight: 700;
        line-height: 1.05;
        color: #f8fafc;
        margin: 20px 0;
    }

    .hero-title span {
        background: linear-gradient(
            90deg,
            #60a5fa,
            #22d3ee
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 16px;
        line-height: 1.7;
        max-width: 650px;
    }

    .status-online {
        display: inline-block;
        color: #4ade80;
        background: rgba(74, 222, 128, 0.08);
        border: 1px solid rgba(74, 222, 128, 0.2);
        border-radius: 30px;
        padding: 7px 13px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .info-strip {
        background: rgba(96, 165, 250, 0.07);
        border: 1px solid rgba(96, 165, 250, 0.15);
        border-radius: 14px;
        padding: 18px;
        color: #cbd5e1;
        margin-top: 20px;
    }

    .file-name {
        overflow-wrap: anywhere;
        word-break: break-word;
        color: #e2e8f0;
    }

    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="margin-bottom: 45px;">

    <div style="
        color: #60a5fa;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 3px;
        margin-bottom: 15px;
    ">
        SMARTBLUR / AI TECHNOLOGY
    </div>

    <div class="status-online">
        ● RENDSZER ONLINE
    </div>

    <div class="hero-title">
        Your privacy.<br>
        <span>Our intelligence.</span>
    </div>

    <div class="hero-subtitle">
        Intelligens képanonimizáló rendszer, amely mesterséges
        intelligencia segítségével automatikusan felismeri és
        elhomályosítja az arcokat és a gépjárművek rendszámait.
    </div>

</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="section-label">
    01 / KÉPFELTÖLTÉS
</div>

<h3 style="margin-bottom: 5px;">
    Válaszd ki a feldolgozandó képet
</h3>

<p style="color: #94a3b8; margin-bottom: 20px;">
    Tölts fel egy képet, amelyen szeretnéd anonimizálni
    az arcokat és a rendszámokat.
</p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Húzd ide a képet, vagy tallózz a fájlok között",
    type=["jpg", "jpeg", "png"],
    help="Támogatott formátumok: JPG, JPEG, PNG"
)
if uploaded_file is None:
    for key in [
        "result",
        "diagnostic",
        "face_count",
        "plate_count",
        "file_id"
    ]:
        st.session_state.pop(key, None)

    st.markdown("""
    <div class="info-strip">
        <strong>Hogyan működik?</strong><br><br>
        1. Tölts fel egy képet.<br>
        2. Indítsd el az AI-alapú felismerést.<br>
        3. A rendszer anonimizálja az arcokat és a rendszámokat.<br>
        4. Töltsd le az elkészült képet.
    </div>
    """, unsafe_allow_html=True)

else:
    current_file_id = (
        uploaded_file.name,
        uploaded_file.size
    )

    if st.session_state.get("file_id") != current_file_id:
        for key in [
            "result",
            "diagnostic",
            "face_count",
            "plate_count"
        ]:
            st.session_state.pop(key, None)

        st.session_state["file_id"] = current_file_id
