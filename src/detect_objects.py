
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

# ============================================================
# OBJEKTUMFELISMERÉS
# ============================================================

print("Objektumok felismerése...")

results = model(image)

print("Objektumfelismerés befejeződött!")


# ============================================================
# FELISMERT OBJEKTUMOK FELDOLGOZÁSA
# ============================================================

print("\nFelismerési eredmények:")

for box in results[0].boxes:
    class_id = int(box.cls[0])
    name = model.names[class_id]
    confidence = float(box.conf[0])

    if name in ["person", "car"]:
        print(f"{name} - Bizonyosság: {confidence:.2%}")

