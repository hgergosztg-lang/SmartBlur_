
# SmartBlur – Képfeldolgozási pipeline dokumentáció

## 1. A pipeline célja

A `pipeline.py` a SmartBlur központi képfeldolgozó modulja.

Feladata a különböző mesterségesintelligencia-modellek összekapcsolása, a felismerési eredmények feldolgozása és az érzékeny képi területek automatikus anonimizálása.

A modul a teljes folyamatot egyetlen `process_image()` függvényen keresztül teszi elérhetővé a Streamlit felhasználói felület számára.

## 2. A feldolgozás folyamata

A pipeline az alábbi lépésekből áll:

1. A bemeneti kép beolvasása.
2. A YuNet arcfelismerő modell előkészítése.
3. Személyek és gépjárművek felismerése YOLO26n segítségével.
4. Arcok felismerése a személyek képkivágásain.
5. Rendszámtáblák felismerése a gépjárművek képkivágásain.
6. Duplikált felismerések kiszűrése.
7. Diagnosztikai kép létrehozása.
8. Gaussian Blur alkalmazása az érzékeny területeken.
9. A feldolgozott képek és statisztikák visszaadása.

## 3. Modellkoordináták kezelése

A felismerőmodellek a képkivágásokon belül határozzák meg az objektumok koordinátáit.

Mivel ezek a képkivágások az eredeti kép különböző pozícióin helyezkednek el, a koordinátákat vissza kell alakítani az eredeti kép koordinátarendszerébe.

A `convert_coordinates()` függvény ezt a feladatot végzi el.

Bemeneti paraméterei:
- x és y: a felismerés helyi koordinátái.
- w és h: a felismerés szélessége és magassága.
- offset_x és offset_y: a képkivágás eltolása az eredeti képen.

## 4. Duplikációszűrés IoU segítségével

A felismerőmodellek esetenként egymást átfedő vagy közel azonos területeket is visszaadhatnak.

A rendszer az Intersection over Union (IoU) módszert használja a duplikációk kiszűrésére.

Az IoU két téglalap metszetének és uniójának területarányát határozza meg.

A `calculate_iou()` függvény kiszámítja ezt az értéket, a `remove_duplicates()` pedig eltávolítja a meghatározott küszöbértéknél nagyobb átfedésű felismeréseket.

Az általános duplikációszűrés küszöbértéke 0,5.

## 5. Arcfelismerési szűrés

Az arcfelismerés során a rendszer a `is_duplicate_face()` függvényt használja.

Ez nemcsak az IoU értékét vizsgálja, hanem a felismert arcterületek középpontjai közötti távolságot is.

A rendszer duplikáltnak tekinti a felismerést, ha:
- az IoU értéke meghaladja a 0,3-at; vagy
- a két középpont távolsága 20 pixelnél kisebb.

## 6. Gaussian Blur anonimizálás

A `blur_region()` függvény feladata az érzékeny képi területek elhomályosítása.

A feldolgozás során:
- meghatározza a felismerési téglalap koordinátáit;
- ellenőrzi, hogy a terület a kép határain belül van-e;
- kivágja a megfelelő képrégiót;
- Gaussian Blur szűrést alkalmaz;
- visszahelyezi az elhomályosított területet az eredeti képbe.

A projektben használt Gaussian Blur paraméterek:
- Kernelméret: 51 × 51 pixel.
- Szórási paraméter: 30.

## 7. Diagnosztikai kép

A rendszer az anonimizálás mellett egy diagnosztikai képet is létrehoz.

A diagnosztikai képen:
- zöld keret jelöli az arcfelismeréseket;
- piros keret jelöli a rendszámfelismeréseket.

Ez segíti a felismerési eredmények vizuális ellenőrzését.

## 8. Visszaadott eredmények

A `process_image()` függvény egy eredményeket tartalmazó szótárat ad vissza.

A visszaadott adatok:

| Kulcs | Tartalom |
|---|---|
| `anonymized` | Anonimizált kép |
| `diagnostic` | Diagnosztikai kép |
| `face_count` | Felismert arcok száma |
| `plate_count` | Felismert rendszámok száma |

Ezeket az adatokat a Streamlit alkalmazás használja fel a képek és a felismerési statisztikák megjelenítésére.

## 9. Összegzés

A pipeline a különálló felismerőmodelleket egy közös képfeldolgozó rendszerré kapcsolja össze.

A koordinátakezelés, a duplikációszűrés és a Gaussian Blur alkalmazásával a SmartBlur automatikus képanonimizálást valósít meg.
