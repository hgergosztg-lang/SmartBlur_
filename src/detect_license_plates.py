

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


# ============================================================
# TESZTKÉP BEOLVASÁSA
# ============================================================

image_path = "images/test.jpg"

image = cv2.imread(image_path)

if image is None:
    print("HIBA: A kép nem található!")
    exit()

print("Tesztkép sikeresen betöltve!")
