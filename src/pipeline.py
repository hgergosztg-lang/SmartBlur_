
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

# ============================================================
# IOU SZÁMÍTÁS
# ============================================================

def calculate_iou(box1, box2):
    """
    Kiszámítja két téglalap metszetének
    és egyesítésének arányát.
    """

    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])

    x2 = min(
        box1[0] + box1[2],
        box2[0] + box2[2]
    )

    y2 = min(
        box1[1] + box1[3],
        box2[1] + box2[3]
    )

    intersection_width = max(0, x2 - x1)
    intersection_height = max(0, y2 - y1)

    intersection = intersection_width * intersection_height

    area1 = box1[2] * box1[3]
    area2 = box2[2] * box2[3]

    union = area1 + area2 - intersection

    if union <= 0:
        return 0

    return intersection / union


# ============================================================
# DUPLIKÁLT TALÁLATOK SZŰRÉSE
# ============================================================

def remove_duplicates(boxes, threshold=0.5):
    """
    Eltávolítja az egymást nagymértékben
    átfedő téglalapokat.
    """

    filtered_boxes = []

    for box in boxes:
        duplicate = False

        for existing_box in filtered_boxes:
            if calculate_iou(box, existing_box) > threshold:
                duplicate = True
                break

        if not duplicate:
            filtered_boxes.append(box)

    return filtered_boxes

# ============================================================
# DUPLIKÁLT ARCFELISMERÉSEK SZŰRÉSE
# ============================================================

def is_duplicate_face(box, existing_faces):
    """
    Kiszűri a már felismert arcok ismételt találatait.
    """

    center_x = box[0] + box[2] / 2
    center_y = box[1] + box[3] / 2

    for existing in existing_faces:
        existing_center_x = existing[0] + existing[2] / 2
        existing_center_y = existing[1] + existing[3] / 2

        distance = (
            (center_x - existing_center_x) ** 2
            + (center_y - existing_center_y) ** 2
        ) ** 0.5

        if calculate_iou(box, existing) > 0.3 or distance < 20:
            return True

    return False


# ============================================================
# GAUSSIAN BLUR ALKALMAZÁSA
# ============================================================

def blur_region(image, box):
    """
    Gaussian blur alkalmazása a megadott képrészleten.
    """

    x, y, w, h = box

    height, width = image.shape[:2]

    x = max(0, x)
    y = max(0, y)

    w = min(w, width - x)
    h = min(h, height - y)

    if w <= 0 or h <= 0:
        return

    region = image[y:y + h, x:x + w]

    if region.size == 0:
        return

    blurred = cv2.GaussianBlur(
        region,
        (51, 51),
        30
    )

    image[y:y + h, x:x + w] = blurred
