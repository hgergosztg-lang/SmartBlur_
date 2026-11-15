
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

    original_image = Image.open(uploaded_file).convert("RGB")

    st.markdown("""
    <div class="section-label">
        02 / KÉP ELŐNÉZETE
    </div>

    <h3 style="margin-bottom: 15px;">
        Feltöltött kép
    </h3>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.image(
            original_image,
            use_container_width=True
        )

    with col2:
        st.markdown("### Fájl információk")

        st.markdown(
            f'<div class="file-name"><strong>Fájlnév:</strong> {uploaded_file.name}</div>',
            unsafe_allow_html=True
        )

        st.write(f"**Méret:** {uploaded_file.size / 1024:.1f} KB")
        st.write(f"**Formátum:** {original_image.format or uploaded_file.type}")
        st.write(f"**Felbontás:** {original_image.width} × {original_image.height}")
            st.markdown("""
    <div class="section-label" style="margin-top: 35px;">
        03 / FELDOLGOZÁS
    </div>

    <h3>
        Készen állsz az anonimizálásra?
    </h3>

    <p style="color: #94a3b8;">
        Indítsd el a mesterséges intelligencia alapú
        képfeldolgozást.
    </p>
    """, unsafe_allow_html=True)

    process_button = st.button(
        "🔒  Kép anonimizálása",
        use_container_width=True
    )
    if process_button:
        try:
            with st.spinner(
                "A mesterséges intelligencia feldolgozza a képet..."
            ):
                images_dir = os.path.join(BASE_DIR, "images")
                os.makedirs(images_dir, exist_ok=True)

                temp_path = os.path.join(
                    images_dir,
                    "uploaded_image.jpg"
                )

                original_image.save(temp_path, format="JPEG")

                results = process_image(temp_path)

                st.session_state["result"] = results["anonymized"]
                st.session_state["diagnostic"] = results["diagnostic"]
                st.session_state["face_count"] = results["face_count"]
                st.session_state["plate_count"] = results["plate_count"]

            st.success("A kép anonimizálása sikeresen befejeződött!")

        except Exception as e:
            st.error(f"Hiba történt a feldolgozás során: {e}")

    if "result" in st.session_state:
        st.markdown("""
        <div class="section-label" style="margin-top: 45px;">
            04 / FELISMERÉSI EREDMÉNYEK
        </div>

        <h3>
            Anonimizálási statisztikák
        </h3>
        """, unsafe_allow_html=True)

        metric1, metric2, metric3 = st.columns(3)

        with metric1:
            st.metric(
                label="Felismerett arcok",
                value=st.session_state["face_count"]
            )

        with metric2:
            st.metric(
                label="Felismerett rendszámok",
                value=st.session_state["plate_count"]
            )

        with metric3:
            total = (
                st.session_state["face_count"]
                + st.session_state["plate_count"]
            )

            st.metric(
                label="Összes anonimizált objektum",
                value=total
            )
        st.markdown("""
        <div class="section-label" style="margin-top: 35px;">
            05 / FELISMERÉSI DIAGNOSZTIKA
        </div>

        <h3>
            AI felismerési eredmények
        </h3>

        <p style="color: #94a3b8;">
            A rendszer által felismert területek
            színes keretekkel megjelölve.
        </p>
        """, unsafe_allow_html=True)

        st.image(
            st.session_state["diagnostic"],
            caption="Zöld keret: arcok | Piros keret: rendszámok",
            use_container_width=True
        )
        st.markdown("""
        <div class="section-label" style="margin-top: 45px;">
            06 / VÉGEREDMÉNY
        </div>

        <h3>
            Eredeti és anonimizált kép összehasonlítása
        </h3>
        """, unsafe_allow_html=True)

        original_col, result_col = st.columns(2)

        with original_col:
            st.markdown("**Eredeti kép**")
            st.image(
                original_image,
                use_container_width=True
            )

        with result_col:
            st.markdown("**Anonimizált kép**")
            st.image(
                st.session_state["result"],
                use_container_width=True
            )
                    st.markdown("""
        <div class="section-label" style="margin-top: 40px;">
            07 / LETÖLTÉS
        </div>

        <h3>
            Töltsd le az elkészült képet
        </h3>

        <p style="color: #94a3b8;">
            Az anonimizált kép készen áll a letöltésre.
        </p>
        """, unsafe_allow_html=True)

        download_buffer = BytesIO()

        Image.fromarray(
            st.session_state["result"]
        ).save(
            download_buffer,
            format="JPEG",
            quality=95
        )

        st.download_button(
            label="⬇️  Anonimizált kép letöltése",
            data=download_buffer.getvalue(),
            file_name="smartblur_anonymized.jpg",
            mime="image/jpeg",
            use_container_width=True
        )
                st.markdown("""
        <div class="info-strip">
            <strong>🔒 Adatvédelem</strong><br><br>
            A SmartBlur célja a személyes adatok védelme.
            A rendszer automatikusan felismeri és elhomályosítja
            az arcokat és a gépjárművek rendszámait.
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="
    margin-top: 70px;
    padding-top: 25px;
    border-top: 1px solid rgba(148, 163, 184, 0.15);
    text-align: center;
    color: #64748b;
    font-size: 12px;
">
    <strong style="color: #94a3b8;">SMARTBLUR</strong>
    <br><br>
    AI-powered image anonymization
    <br>
    © 2026 SmartBlur Project
</div>
""", unsafe_allow_html=True)
