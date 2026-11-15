
# SmartBlur – Tesztelési dokumentáció

## 1. A tesztelés célja

A tesztelés célja a SmartBlur képanonimizáló rendszer egyes komponenseinek és teljes működésének ellenőrzése.

A tesztelés során külön vizsgáljuk az objektumfelismerést, az arcfelismerést, a rendszámfelismerést, valamint az integrált képfeldolgozási folyamatot.

## 2. Tesztkörnyezet

| Tulajdonság | Érték |
|---|---|
| Programozási nyelv | Python |
| Felhasználói felület | Streamlit |
| Objektumfelismerés | YOLO26n |
| Arcfelismerés | YuNet |
| Rendszámfelismerés | YOLOv8n |
| Képfeldolgozás | OpenCV |
| Tesztképek formátuma | JPG, JPEG, PNG |

## 3. Elvégzett tesztek

### 3.1. Objektumfelismerés

A `detect_objects.py` modul ellenőrzi a YOLO26n modell működését.

Vizsgált funkciók:
- Tesztkép betöltése.
- Személyek felismerése.
- Gépjárművek felismerése.
- Felismerési eredmények megjelenítése.
- Diagnosztikai kép mentése.

### 3.2. Rendszámfelismerés

A `detect_license_plates.py` modul a rendszámfelismerő modell működését vizsgálja.

Vizsgált funkciók:
- Modell betöltése.
- Tesztkép feldolgozása.
- Rendszámtáblák helyének meghatározása.
- Felismerési bizonyosság megjelenítése.
- Eredménykép mentése.

### 3.3. Arcfelismerés

A `detect_faces.py` modul a YuNet modell működését ellenőrzi.

Vizsgált funkciók:
- ONNX modell betöltése.
- Arcok felismerése.
- Felismert arcok körül keretek rajzolása.
- Felismerési bizonyosság megjelenítése.
- Eredménykép mentése.

### 3.4. Integrált képfeldolgozás

A `pipeline.py` modul a három felismerési folyamatot egyesíti.

Vizsgált funkciók:
- Személyek és gépjárművek felismerése.
- Arcok és rendszámok lokalizálása.
- Duplikált felismerések szűrése.
- Gaussian Blur alkalmazása.
- Anonimizált kép előállítása.
- Felismerési statisztikák visszaadása.

### 3.5. Felhasználói felület

Az `app.py` modul a Streamlit felületen keresztül biztosítja a rendszer használatát.

Vizsgált funkciók:
- Képfeltöltés.
- Kép előnézetének megjelenítése.
- Anonimizálás elindítása.
- Eredmények és statisztikák megjelenítése.
- Eredeti és anonimizált kép összehasonlítása.
- Eredmény letöltése.

## 4. Teszteredmények

Az alábbi táblázat a tényleges tesztelés során tölthető ki.

| Teszteset | Elvárt eredmény | Tényleges eredmény |
|---|---|---|
| Tesztkép betöltése | Kép sikeres beolvasása | Kitöltendő |
| Objektumfelismerés | Személyek és autók felismerése | Kitöltendő |
| Arcfelismerés | Arcok lokalizálása | Kitöltendő |
| Rendszámfelismerés | Rendszámok lokalizálása | Kitöltendő |
| Anonimizálás | Felismert területek elhomályosítása | Kitöltendő |
| Kép letöltése | Eredmény sikeres letöltése | Kitöltendő |

## 5. Korlátok

A felismerési eredmények függnek a tesztképek minőségétől, a megvilágítástól, a tárgyak méretétől és láthatóságától.

A rendszámfelismerés a már azonosított gépjárművek területén történik, ezért a gépjármű-felismerés hibája a rendszámfelismerést is befolyásolhatja.

## 6. Összegzés

A tesztelés célja annak igazolása, hogy a SmartBlur komponensei együtt képesek automatikusan felismerni és anonimizálni az érzékeny képi információkat.

A tényleges teszteredmények a fejlesztés és ellenőrzés során kerülnek rögzítésre.
