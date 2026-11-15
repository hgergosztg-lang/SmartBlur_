
# SmartBlur – Rendszerarchitektúra

## 1. Áttekintés

A SmartBlur egy moduláris felépítésű, Python alapú képanonimizáló alkalmazás.

A rendszer három fő részből áll:

- Felhasználói felület.
- Képfeldolgozó logika.
- Mesterségesintelligencia-modellek.

A komponensek különálló feladatokat látnak el, de egy közös feldolgozási folyamatban működnek együtt.

## 2. A rendszer komponensei

### 2.1. Felhasználói felület – app.py

A Streamlit alapú felhasználói felület biztosítja a rendszer kezelését.

Feladatai:
- Képek feltöltése.
- Feltöltött képek előnézete.
- Feldolgozás elindítása.
- Eredmények megjelenítése.
- Felismerési statisztikák megjelenítése.
- Anonimizált képek letöltése.

### 2.2. Képfeldolgozó modul – pipeline.py

A pipeline a rendszer központi feldolgozó egysége.

Feladatai:
- AI-modellek betöltése.
- Objektumok felismerése.
- Arcok és rendszámok lokalizálása.
- Koordináták átalakítása.
- Duplikációk szűrése.
- Diagnosztikai kép létrehozása.
- Érzékeny területek elhomályosítása.

### 2.3. AI-modellek

A rendszer három előre betanított modellt használ:

| Modell | Feladat |
|---|---|
| YOLO26n | Személyek és gépjárművek felismerése |
| YuNet | Arcok felismerése |
| YOLOv8n License Plate | Rendszámtáblák felismerése |

## 3. Adatáramlás

A rendszer adatfeldolgozása a következő módon történik:

```text
Felhasználó
    |
    v
Streamlit felület
    |
    v
Kép feltöltése
    |
    v
app.py
    |
    v
process_image()
    |
    v
pipeline.py
    |
    +----------------------+
    |                      |
    v                      v
 YOLO26n                Képfeldolgozás
    |
    +----------------------+
    |
    v
Személyek és autók felismerése
    |
    +----------------------+
    |                      |
    v                      v
 YuNet             YOLOv8n rendszámmodell
    |                      |
    v                      v
Arcok felismerése   Rendszámok felismerése
    |                      |
    +----------+-----------+
               |
               v
       Duplikációszűrés
               |
               v
         Gaussian Blur
               |
               v
       Anonimizált kép
               |
               v
       Streamlit felület
               |
               v
       Eredmény letöltése
```

## 4. Modulok közötti kapcsolat

Az `app.py` a `process_image()` függvény meghívásával indítja el a feldolgozást.

A `pipeline.py` elvégzi a képfeldolgozási feladatokat, majd visszaadja az eredményeket.

A felhasználói felület ezek alapján jeleníti meg:
- Az anonimizált képet.
- A diagnosztikai képet.
- A felismert arcok számát.
- A felismert rendszámok számát.

## 5. Tesztelő modulok

A projekt három különálló tesztelő modult is tartalmaz:

- `detect_objects.py`
- `detect_faces.py`
- `detect_license_plates.py`

Ezek segítségével a modellek külön-külön is ellenőrizhetők, így a teljes rendszer integrációja előtt vizsgálható az egyes felismerési feladatok működése.

## 6. Összegzés

A moduláris architektúra lehetővé teszi, hogy az egyes komponensek külön fejleszthetők és ellenőrizhetők legyenek.

A felhasználói felület, a képfeldolgozó pipeline és az AI-modellek elkülönítése átláthatóbbá és könnyebben karbantarthatóvá teszi a projektet.
