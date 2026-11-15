
# SmartBlur – AI modellek műszaki dokumentációja

## 1. A modellek szerepe

A SmartBlur három előre betanított mesterségesintelligencia-modellt használ az érzékeny képi információk felismerésére.

A modellek különböző feladatokat látnak el, majd eredményeik egy közös képfeldolgozó folyamatba kerülnek.

## 2. YOLO26n – Objektumfelismerés

A YOLO26n modell feladata a képen található személyek és gépjárművek felismerése.

A rendszer a következő objektumkategóriákat használja:

- Person – emberi személyek.
- Car – személygépkocsik.

A modell által meghatározott objektumterületek alapján történik a további részletes felismerés.

**Felhasználás a projektben:**
- Személyek lokalizálása.
- Gépjárművek lokalizálása.
- A további felismerési folyamatok területének meghatározása.

Modell: `yolo26n.pt`

Forrás: https://docs.ultralytics.com/models/yolo26/

## 3. YuNet – Arcfelismerés

A YuNet egy könnyű, neurális hálózaton alapuló arcfelismerő modell.

A SmartBlur az OpenCV FaceDetectorYN interfészén keresztül használja a modellt.

A felismerés a YOLO26n által azonosított személyek képkivágásain történik.

A modell meghatározza az arcok helyét, valamint a felismeréshez tartozó bizonyossági értéket.

**Felhasználás a projektben:**
- Arcok felismerése.
- Arcterületek koordinátáinak meghatározása.
- Felismerési bizonyosság kezelése.

Modell: `face_detection_yunet_2023mar.onnx`

Forrás: https://github.com/opencv/opencv_zoo

## 4. YOLOv8n – Rendszámfelismerés

A rendszámfelismerő modell egy előre betanított YOLOv8n alapú modell.

Feladata a gépjárművek rendszámtábláinak helymeghatározása.

A felismerés a YOLO26n által azonosított gépjárművek képkivágásain történik.

A modell a rendszámtábla körüli koordinátákat és a felismerés bizonyosságát adja vissza.

**Felhasználás a projektben:**
- Rendszámtáblák lokalizálása.
- Rendszámterületek koordinátáinak meghatározása.
- Felismerési bizonyosság kezelése.

Modell: `license_plate.pt`

Forrás: https://huggingface.co/joker5914/yolov8n-license-plate

**Fontos:** a modell a rendszámtábla helyét ismeri fel, nem olvassa ki a rajta szereplő karaktereket. OCR-funkciót a jelenlegi rendszer nem tartalmaz.

## 5. A modellek együttműködése

A három modell egymásra épülő módon működik.

```text
                 Bemeneti kép
                      |
                      v
                YOLO26n modell
                      |
             +--------+--------+
             |                 |
             v                 v
        Személyek          Autók
             |                 |
             v                 v
        YuNet modell     YOLOv8n modell
             |                 |
             v                 v
        Arcterületek      Rendszámok
             |                 |
             +--------+--------+
                      |
                      v
             Duplikációszűrés
                      |
                      v
               Gaussian Blur
                      |
                      v
             Anonimizált kép
```

## 6. Képfeldolgozás

A felismerőmodellek által visszaadott koordináták alapján a rendszer meghatározza az anonimizálandó képrészleteket.

A feldolgozás során OpenCV Gaussian Blur algoritmust alkalmaz.

A projektben használt eljárás:
- 51 × 51 méretű Gauss-kernel.
- 30-as szórási paraméter.

A rendszer az eredeti kép megfelelő régióit elhomályosított változattal helyettesíti.

## 7. Összegzés

A SmartBlur több különböző feladatokra specializált, előre betanított modellt kapcsol össze.

A YOLO26n végzi az általános objektumfelismerést, a YuNet az arcok felismerését, míg a YOLOv8n alapú modell a rendszámtáblák helyét határozza meg.

A felismerési eredményeket egy közös képfeldolgozó folyamat használja fel az automatikus anonimizáláshoz.
