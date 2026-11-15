
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


# ============================================================
# TESZTKÉP BEOLVASÁSA
# ============================================================

image_path = "images/test.jpg"

image = cv2.imread(image_path)

if image is None:
    print("HIBA: A kép nem található!")
    exit()

print("Tesztkép sikeresen betöltve!")
