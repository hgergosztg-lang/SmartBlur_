

# ============================================================
# SZÜKSÉGES KÖNYVTÁRAK IMPORTÁLÁSA
# ============================================================

from ultralytics import YOLO
import cv2
import os


# ============================================================
# RENDSZÁMFELISMERŐ MODELL BETÖLTÉSE
# ============================================================

print("Rendszámfelismerő modell betöltése...")

model = YOLO("models/license_plate.pt")

print("Rendszámfelismerő modell sikeresen betöltve!")
