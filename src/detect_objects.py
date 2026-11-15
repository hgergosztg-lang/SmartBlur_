
# ============================================================
# SZÜKSÉGES KÖNYVTÁRAK IMPORTÁLÁSA
# ============================================================

from ultralytics import YOLO
import cv2
import os


# ============================================================
# YOLO MODELL BETÖLTÉSE
# ============================================================

print("YOLO modell betöltése...")

model = YOLO("yolo26n.pt")

print("YOLO modell sikeresen betöltve!")

