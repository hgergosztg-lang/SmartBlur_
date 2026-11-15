
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
