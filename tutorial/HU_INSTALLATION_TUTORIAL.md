# Telepítési útmutató

## Előkészület

A Zebra Label Printer telepítése előtt ellenőrizd, hogy az üzlet megfelel a kompatibilitási követelményeknek.
Ellenőrizd, hogy a Zebra nyomtató hálózaton van-e: nyomd meg az X gombot a nyomtatón. Ha a hálózat (Ethernet) ikon zöld, akkor a nyomtató csatlakoztatva van.

| Állapot | Kép |
|--------|-----|
| A nyomtató használható NET/TCP és USB módban is | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/OK.JPEG" alt="Zebra nyomtató hálózati állapot" width="420" /> |
| A nyomtató nincs hálózatra csatlakoztatva — csak USB módban működik | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/NO_NETWORK.JPEG" alt="Zebra nyomtató hálózati állapot – nincs kapcsolat" width="420" /> |

**Ha hálózati problémát tapasztalsz, ellenőrizd az alábbiakat:**

Győződj meg róla, hogy az Ethernet kábel be van dugva a nyomtató alábbi portjába:

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/CABLE.png" alt="Zebra nyomtató Ethernet port" width="420" />

## Telepítés lépései

1. Töltsd le a legfrissebb `zlp-installer.exe` verziót a kiadások oldaláról. (Az alábbi linken a letöltési oldalra jutsz.)

    [zlp-installer.exe letöltése](https://github.com/TMarccci/Zebra-Label-Printer/releases/latest)

2. Indítsd el az alkalmazást, és fogadd el a Windows SmartScreen figyelmeztetést, ha megjelenik.

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SMART_SCREEN_ACCEPT.png" alt="Windows SmartScreen figyelmeztetés" width="520" />

3. Kövesd a képernyőn megjelenő utasításokat.
4. Fejezd be a telepítő varázslót (ha tovább tart, az normális — nyugodtan igyál egy kávét ☕).

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/INSTALLER.png" alt="Zebra Label Printer telepítő varázsló" width="520" />

5. Indítsd el az alkalmazást az asztali ikonról vagy a Start menüből. (Ha a telepítés után nem nyílt meg automatikusan.)

## Első beállítás

Az alkalmazás tetején 3 oldal van: **Main**, **Server Settings**, **Currency**.

1. Nyisd meg a `Zebra Label Printer.exe` fájlt (ha nem indult el automatikusan a telepítés után).
2. Menj a **Server Settings** oldalra.

### A opció: NET/TCP (hálózati nyomtató)

1. A **Print Mode** legyen `NET/TCP`.
2. Kattints a `Find Printers` gombra a hálózati Zebra nyomtatók kereséséhez.
3. Válaszd ki/írd be a nyomtató IP címét (és a portot, általában `9100`).
4. Kattints a `Test Printer` gombra.
5. Kattints a `Save Configuration` gombra (alul).

### B opció: USB (helyi USB nyomtató)

1. A **Print Mode** legyen `USB`.
2. Válaszd ki a Zebra nyomtatót a legördülő listából.
3. Ha nem látod, kattints a `Refresh` gombra.
4. Kattints a `Test Printer` gombra.
5. Kattints a `Save Configuration` gombra (alul).

### Pénznem

1. Menj a **Currency** oldalra.
2. Állítsd be a pénznemet, árjavaslat típusát és a tizedeseket.
3. Kattints a `Save Configuration` gombra (alul).

### Nyomtatás indítása

1. Menj a **Main** oldalra.
2. Kattints a `Start Server` gombra (ha nem indult el automatikusan).
3. Kattints az `Open Printer Page` gombra.

(Példa oldalak)

| Oldal | Kép |
|------|-----|
| Main | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_1.png" alt="Zebra Label Printer - Main oldal" width="520" /> |
| Server Settings | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_2.png" alt="Zebra Label Printer - Server Settings oldal" width="520" /> |
| Currency | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_3.png" alt="Zebra Label Printer - Currency oldal" width="520" /> |

---

**Megjegyzések:**
- Ha bármilyen problémát tapasztalsz a telepítés vagy beállítás során, nézd meg a README.md hibaelhárítás részét, vagy vedd fel a kapcsolatot a támogatással.
- Ha a telepítésnél az alapértelmezett beállításokat hagytad, az alkalmazás létrehoz egy asztali ikont, és a Windowszal együtt indul. (Elég az `Open Printer Page` gombra kattintani a használat elkezdéséhez.)
- A webes felület hivatkozását elmentheted könyvjelzőként a böngészőben.

Tipp: Ha mentés nélkül próbálsz oldalt váltani, az app rákérdez: Save / Discard / Cancel.

## Az első címke nyomtatása

1. A webes felületen válaszd ki az ár módot: „SALE PRICE” (akciós ár) vagy „NORMAL PRICE” (normál ár).
2. Add meg az árat a javaslat gombokkal vagy kézzel beírva.
3. Állítsd be a nyomtatandó címkék mennyiségét (alapértelmezés szerint 1, ha nincs megadva).
4. Kattints a `Submit` gombra a címke nyomtatásához.
5. Ellenőrizd, hogy a címke megfelelően kinyomtatódott a Zebra nyomtatón.

(Webes felület képernyőképe)

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SCREENSHOT.png" alt="Zebra Label Printer webes felület" />


**Gratulálunk!** Sikeresen telepítetted és beállítottad a Zebra Label Printer alkalmazást. Mostantól hatékonyan nyomtathatsz ár címkéket a webes felületen keresztül.