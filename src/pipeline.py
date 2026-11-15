
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


# ============================================================
# YUNET MODELL ELŐKÉSZÍTÉSE
# ============================================================

def prepare_face_model():

    # Ellenőrizzük, hogy az eredeti modell létezik-e.
    if not os.path.exists(FACE_MODEL_SOURCE_PATH):
        raise FileNotFoundError(
            f"Nem található az arcfelismerő modell: "
            f"{FACE_MODEL_SOURCE_PATH}"
        )

    # Célmappa létrehozása.
    os.makedirs(FACE_MODEL_DIR, exist_ok=True)

    source_size = os.path.getsize(
        FACE_MODEL_SOURCE_PATH
    )

    # Ellenőrizzük, szükséges-e a modell másolása.
    target_needs_copy = (
        not os.path.exists(FACE_MODEL_PATH)
        or os.path.getsize(FACE_MODEL_PATH) != source_size
    )

    if target_needs_copy:
        shutil.copyfile(
            FACE_MODEL_SOURCE_PATH,
            FACE_MODEL_PATH
        )

    if not os.path.exists(FACE_MODEL_PATH):
        raise FileNotFoundError(
            f"A YuNet modell nem található: {FACE_MODEL_PATH}"
        )

    print(
        f"YuNet modell előkészítve: {FACE_MODEL_PATH}"
    )

# ============================================================
# AI-MODELLEK BETÖLTÉSE
# ============================================================

print("SmartBlur modellek betöltése...")

# YOLO26n objektumfelismerő modell
object_model = YOLO(OBJECT_MODEL_PATH)

# YOLO rendszámfelismerő modell
plate_model = YOLO(PLATE_MODEL_PATH)

# YuNet modell előkészítése
prepare_face_model()

print("SmartBlur modellek sikeresen betöltve!")


# ============================================================
# KOORDINÁTÁK ÁTALAKÍTÁSA
# ============================================================

def convert_coordinates(x, y, w, h, offset_x, offset_y):
    """
    A kivágott kép koordinátáit visszaalakítja
    az eredeti kép koordinátáira.
    """

    return (
        int(x + offset_x),
        int(y + offset_y),
        int(w),
        int(h)
    )
