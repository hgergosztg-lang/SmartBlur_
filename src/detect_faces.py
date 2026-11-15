

# ============================================================
# SZÜKSÉGES KÖNYVTÁRAK IMPORTÁLÁSA
# ============================================================

import cv2
import os


# ============================================================
# YUNET MODELL ELÉRÉSI ÚTVONALA
# ============================================================

model_path = "models/face_detection_yunet_2023mar.onnx"


# ============================================================
# TESZTKÉP BEOLVASÁSA
# ============================================================

image_path = "images/test.jpg"

image = cv2.imread(image_path)

if image is None:
    print("HIBA: A kép nem található!")
    exit()

print("Tesztkép sikeresen betöltve!")
