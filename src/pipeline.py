
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

# ============================================================
# FŐ KÉPFELDOLGOZÓ FÜGGVÉNY
# ============================================================

def process_image(image_path):

    print("\nSmartBlur feldolgozás elindult!")

    # --------------------------------------------------------
    # 1. EREDETI KÉP BETÖLTÉSE
    # --------------------------------------------------------

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(
            f"A kép nem tölthető be: {image_path}"
        )

    height, width = image.shape[:2]

    print(f"Kép mérete: {width} x {height}")

    # --------------------------------------------------------
    # 2. YUNET ARCFELISMERŐ MODELL ELŐKÉSZÍTÉSE
    # --------------------------------------------------------

    face_detector = cv2.FaceDetectorYN.create(
        FACE_MODEL_PATH,
        "",
        (320, 320),
        0.7,
        0.3,
        5000
    )

    # --------------------------------------------------------
    # 3. EMBEREK ÉS AUTÓK FELISMERÉSE YOLO SEGÍTSÉGÉVEL
    # --------------------------------------------------------

    print("\n1. modell: Emberek és autók felismerése...")

    object_results = object_model(
        image,
        conf=0.10,
        iou=0.45,
        max_det=300,
        verbose=False
    )

    person_boxes = []
    car_boxes = []

    for result in object_results:
        for box in result.boxes:

            class_id = int(box.cls[0])

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            x1 = max(0, x1)
            y1 = max(0, y1)

            x2 = min(width, x2)
            y2 = min(height, y2)

            box_width = x2 - x1
            box_height = y2 - y1

            if box_width <= 0 or box_height <= 0:
                continue

            # COCO 0 = személy
            if class_id == 0:
                person_boxes.append(
                    (x1, y1, box_width, box_height)
                )

            # COCO 2 = autó
            elif class_id == 2:
                car_boxes.append(
                    (x1, y1, box_width, box_height)
                )

    person_boxes = remove_duplicates(
        person_boxes,
        threshold=0.45
    )

    car_boxes = remove_duplicates(
        car_boxes,
        threshold=0.55
    )

    print(f"Ember régiók: {len(person_boxes)}")
    print(f"Autó régiók: {len(car_boxes)}")

    # --------------------------------------------------------
    # 4. ARCFELISMERÉS YUNET SEGÍTSÉGÉVEL
    # --------------------------------------------------------

    print("\n2. modell: Arcok felismerése...")

    face_boxes = []

    for person_box in person_boxes:

        x, y, w, h = person_box

        person_crop = image[
            y:y + h,
            x:x + w
        ]

        if person_crop.size == 0:
            continue

        crop_height, crop_width = person_crop.shape[:2]

        face_detector.setInputSize(
            (crop_width, crop_height)
        )

        _, faces = face_detector.detect(person_crop)

        if faces is None:
            continue

        for face in faces:

            fx = int(face[0])
            fy = int(face[1])
            fw = int(face[2])
            fh = int(face[3])

            full_face_box = convert_coordinates(
                fx,
                fy,
                fw,
                fh,
                x,
                y
            )

            if not is_duplicate_face(
                full_face_box,
                face_boxes
            ):
                face_boxes.append(full_face_box)

    print(f"Felismert arcok: {len(face_boxes)}")
    
    # --------------------------------------------------------
    # 5. RENDSZÁMFELISMERÉS
    # --------------------------------------------------------

    print("\n3. modell: Rendszámok felismerése...")

    plate_boxes = []

    for car_box in car_boxes:

        x, y, w, h = car_box

        car_crop = image[
            y:y + h,
            x:x + w
        ]

        if car_crop.size == 0:
            continue

        plate_results = plate_model(
            car_crop,
            conf=0.25,
            iou=0.45,
            verbose=False
        )

        for result in plate_results:

            for box in result.boxes:

                px1, py1, px2, py2 = map(
                    int,
                    box.xyxy[0].tolist()
                )

                plate_width = px2 - px1
                plate_height = py2 - py1

                if plate_width <= 0 or plate_height <= 0:
                    continue

                full_plate_box = convert_coordinates(
                    px1,
                    py1,
                    plate_width,
                    plate_height,
                    x,
                    y
                )

                plate_boxes.append(full_plate_box)

    plate_boxes = remove_duplicates(
        plate_boxes,
        threshold=0.35
    )

    print(f"Felismert rendszámok: {len(plate_boxes)}")

    # --------------------------------------------------------
    # 6. DIAGNOSZTIKAI KÉP ELKÉSZÍTÉSE
    # --------------------------------------------------------

    diagnostic_image = image.copy()

    # Arcok: zöld keret
    for box in face_boxes:

        x, y, w, h = box

        cv2.rectangle(
            diagnostic_image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    # Rendszámok: piros keret
    for box in plate_boxes:

        x, y, w, h = box

        cv2.rectangle(
            diagnostic_image,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )


    # --------------------------------------------------------
    # 7. ANONIMIZÁLÁS
    # --------------------------------------------------------

    print("\nAnonimizálás folyamatban...")

    anonymized_image = image.copy()

    for box in face_boxes:
        blur_region(anonymized_image, box)

    for box in plate_boxes:
        blur_region(anonymized_image, box)

    # --------------------------------------------------------
    # 8. EREDMÉNYEK MENTÉSE
    # --------------------------------------------------------

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cv2.imwrite(
        os.path.join(OUTPUT_DIR, "pipeline_result.jpg"),
        diagnostic_image
    )

    cv2.imwrite(
        os.path.join(OUTPUT_DIR, "anonymized.jpg"),
        anonymized_image
    )

    # --------------------------------------------------------
    # 9. FELISMERÉSI STATISZTIKÁK
    # --------------------------------------------------------

    face_count = len(face_boxes)
    plate_count = len(plate_boxes)

    print("\n========== SMARTBLUR EREDMÉNY ==========")

    print(f"Felismert arcok: {face_count}")
    print(f"Felismert rendszámok: {plate_count}")

    print("\nEredményfájlok:")
    print(os.path.join(OUTPUT_DIR, "pipeline_result.jpg"))
    print(os.path.join(OUTPUT_DIR, "anonymized.jpg"))

    print("\nSmartBlur feldolgozás befejeződött!")

    # --------------------------------------------------------
    # 10. EREDMÉNYEK VISSZAADÁSA A STREAMLITNEK
    # --------------------------------------------------------

    return {
        "anonymized": cv2.cvtColor(
            anonymized_image,
            cv2.COLOR_BGR2RGB
        ),
        "diagnostic": cv2.cvtColor(
            diagnostic_image,
            cv2.COLOR_BGR2RGB
        ),
        "face_count": face_count,
        "plate_count": plate_count
    }
