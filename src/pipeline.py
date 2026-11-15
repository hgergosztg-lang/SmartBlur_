
# ============================================================
# SZÜKSÉGES KÖNYVTÁRAK IMPORTÁLÁSA
# ============================================================

import os
import shutil
import cv2

from ultralytics import YOLO


# ============================================================
# PROJEKT ÉS MODELLÚTVONALAK
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# YOLO26n objektumfelismerő modell
OBJECT_MODEL_PATH = os.path.join(
    BASE_DIR,
    "yolo26n.pt"
)

# Rendszámfelismerő modell
PLATE_MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "license_plate.pt"
)

# YuNet arcfelismerő modell eredeti helye
FACE_MODEL_SOURCE_PATH = os.path.join(
    BASE_DIR,
    "models",
    "face_detection_yunet_2023mar.onnx"
)

# YuNet modell ékezetmentes elérési útvonala
FACE_MODEL_DIR = r"C:\SmartBlurModels"

FACE_MODEL_PATH = os.path.join(
    FACE_MODEL_DIR,
    "face_detection_yunet_2023mar.onnx"
)

# Feldolgozott képek mentési helye
OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

