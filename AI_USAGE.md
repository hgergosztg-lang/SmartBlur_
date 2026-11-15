
# SmartBlur – Mesterséges intelligencia használatának dokumentációja

## 1. Felhasznált AI-eszköz

A SmartBlur fejlesztése során az OpenAI által készített ChatGPT mesterségesintelligencia-alapú eszközt használtam fejlesztési segítségként.

Az eszköz elsősorban programozási feladatok megvalósításában, a felhasznált modellek működésének megértésében és a fejlesztés során felmerülő hibák keresésében nyújtott segítséget.

## 2. Programozási segítség

A projekt forráskódjának elkészítése során a feladatok egy részét önállóan valósítottam meg, míg bizonyos programozási megoldások kidolgozásában ChatGPT segítségét vettem igénybe.

A segítség elsősorban az alábbi területekre terjedt ki:

- Python-függvények megvalósítása.
- YuNet arcfelismerés használata OpenCV segítségével.
- Koordinátakezelési megoldások kialakítása.
- IoU-alapú duplikációszűrés megvalósítása.
- Gaussian Blur képfeldolgozás alkalmazása.

A kapott kódrészleteket a projekt meglévő felépítéséhez igazítottam, majd a helyi fejlesztőkörnyezetben ellenőriztem.

## 3. Modellek megértése és technikai segítség

A ChatGPT segítséget nyújtott a projektben alkalmazott technológiák és algoritmusok működésének megértésében.

Különösen az alábbi témákban:

- YOLO objektumfelismerő modellek működése.
- YuNet arcfelismerő modell használata.
- Rendszámtáblák felismerésének folyamata.
- OpenCV képfeldolgozási lehetőségei.
- IoU-alapú duplikációszűrés működése.
- Gaussian Blur algoritmus működése és alkalmazása.
- A különböző AI-modellek összekapcsolása egy közös képfeldolgozó folyamatban.

## 4. Hibakeresés

A fejlesztés során a ChatGPT segítséget nyújtott a felmerülő programozási hibák elemzésében és a lehetséges javítási megoldások megtalálásában.

A hibakeresés többek között az alábbi területeket érintette:

- AI-modellek betöltésével kapcsolatos problémák.
- Fájlútvonalak és modellútvonalak kezelése.
- OpenCV és YuNet integrációs problémák.
- Python-függvények működésével kapcsolatos hibák.
- Streamlit felhasználói felület működése.
- A képfeldolgozó pipeline egyes lépéseinek ellenőrzése.

A javasolt módosításokat a helyi fejlesztőkörnyezetben teszteltem.

## 5. Konkrét fejlesztési példák

### 5.1. YOLO modell integrálása

**Feladat:** Objektumfelismerés megvalósítása Pythonban.

**Felhasznált eszköz:** ChatGPT.

**Prompt:** Hogyan lehet YOLO segítségével személyeket és gépjárműveket felismerni egy képen?

**Kapott eredmény:** Segítséget kaptam a YOLO modell betöltéséhez, a képfeldolgozás elindításához és a felismerési eredmények feldolgozásához.

**Ellenőrzés:** A megoldást tesztképeken ellenőriztem, és a projekt felépítéséhez igazítottam.

### 5.2. Arcfelismerés megvalósítása

**Feladat:** YuNet modell használata OpenCV segítségével.

**Prompt:** Hogyan lehet OpenCV FaceDetectorYN segítségével arcokat felismerni egy képen?

**Kapott eredmény:** Segítséget kaptam az ONNX modell betöltéséhez, a felismerés elindításához és az arcterületek koordinátáinak kezeléséhez.

**Ellenőrzés:** A felismerést helyi tesztképeken ellenőriztem.

### 5.3. Hibakeresés

**Feladat:** A képfeldolgozó rendszer működése során felmerülő hibák javítása.

**Prompt:** Segíts a Python képfeldolgozó kódban jelentkező hiba elemzésében és javításában.

**Kapott eredmény:** Hibakeresési javaslatokat és lehetséges megoldásokat kaptam.

**Ellenőrzés:** A módosításokat a helyi fejlesztőkörnyezetben teszteltem.

*Megjegyzés: A fenti promptok a felhasznált utasítások tartalmát összefoglaló példák.*

## 6. Ellenőrzés és tesztelés

A fejlesztés során a kapott kódokat és javaslatokat nem tekintettem automatikusan hibátlannak.

A megoldásokat a helyi Python-környezetben ellenőriztem, és a működést valódi tesztképekkel vizsgáltam.

A tesztelés során ellenőriztem:

- Az objektumfelismerés működését.
- Az arcfelismerést.
- A rendszámtáblák felismerését.
- Az automatikus anonimizálást.
- A diagnosztikai kép létrehozását.
- A Streamlit felhasználói felület működését.

A tesztelés során az alkalmazás sikeresen felismerte és elhomályosította az arcokat és a rendszámtáblákat.

## 7. Összegzés

A ChatGPT a SmartBlur fejlesztése során programozási, technikai és hibakeresési segítséget biztosított.

A projekt egyes kódrészei önálló munkával, más részei AI segítségével készültek.

Az AI-eszköz támogatta a fejlesztési folyamatot, azonban a kapott megoldások integrálása és működésük ellenőrzése a projekt megvalósításának részét képezte.
