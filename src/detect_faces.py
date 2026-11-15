

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


# ============================================================
# YUNET ARCFELISMERŐ MODELL LÉTREHOZÁSA
# ============================================================

height, width = image.shape[:2]

detector = cv2.FaceDetectorYN.create(
    model_path,
    "",
    (width, height),
    0.7,
    0.3,
    5000
)

print("YuNet arcfelismerő modell sikeresen inicializálva!")


# ============================================================
# ARCFELISMERÉS
# ============================================================

print("Arcfelismerés folyamatban...")

_, faces = detector.detect(image)


# ============================================================
# FELISMERT ARCOK FELDOLGOZÁSA
# ============================================================

if faces is not None:
    print(f"Felismert arcok száma: {len(faces)}")

    for face in faces:
        x, y, w, h = face[:4].astype(int)
        confidence = face[14]

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        print(f"Arc - Bizonyosság: {confidence:.2%}")

else:
    print("Nem található arc a képen.")


# ============================================================
# FELISMERT ARCOK EREDMÉNYÉNEK MENTÉSE
# ============================================================

os.makedirs("output", exist_ok=True)

cv2.imwrite("output/faces.jpg", image)

print("Kész! Eredmény: output/faces.jpg")
