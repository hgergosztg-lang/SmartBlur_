

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


# ============================================================
# RENDSZÁMFELISMERÉS
# ============================================================

print("Rendszámok keresése...")

results = model(image)

print("Rendszámfelismerés befejeződött!")

# ============================================================
# FELISMERT RENDSZÁMOK FELDOLGOZÁSA
# ============================================================

print("\nFelismerési eredmények:")

if len(results[0].boxes) > 0:

    for box in results[0].boxes:
        confidence = float(box.conf[0])

        x1, y1, x2, y2 = box.xyxy[0].int().tolist()

        print(f"Rendszám - Bizonyosság: {confidence:.2%}")

else:
    print("Nem található rendszám a képen.")

