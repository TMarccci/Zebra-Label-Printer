# Telepítési útmutató

## Telepítés lépései

0. Előfeltételek:
   - A legjobb élményhez használd a Google Chrome-ot.

1. Töltsd le a legfrissebb `zlp-installer.exe` verziót a kiadások oldaláról. Ahogy az alábbi képen látható. (Kattints az alábbi gombra a letöltési oldal megnyitásához):
    
   [https://github.com/TMarccci/Zebra-Label-Printer/releases/latest](https://github.com/TMarccci/Zebra-Label-Printer/releases/latest)

   <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/FILE.png" alt="Letöltési oldal" width="520" />

   | Microsoft Edge használatakor egy ilyen figyelmeztetés megjelenhet: | Kövesd a „Keep” lépéseket a letöltés folytatásához. |
   |---------------------------------------------------------------|--------------------------------------------------------------------------------|
   | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/EDGE_WARNING.png" alt="Microsoft Edge figyelmeztetés" /> | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/EDGE_WARNING_2.png" alt="Microsoft Edge - Keep File"/> |

2. Indítsd el az alkalmazást, és fogadd el a Windows SmartScreen figyelmeztetést, ha megjelenik.

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SMART_SCREEN_ACCEPT.png" alt="Windows SmartScreen figyelmeztetés" width="520" />

3. Kövesd a képernyőn megjelenő utasításokat.
4. Fejezd be a telepítő varázslót (ne aggódj, ha kicsit tovább tart — ez normális. Igyál egy kávét ☕, amíg vársz. 😉)

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/INSTALLER.png" alt="Zebra Label Printer telepítő varázsló" width="300" />

## Első beállítás

1. Nyisd meg a `Zebra Label Printer.exe` fájlt (ha a telepítés után nem indult el automatikusan).

Az alkalmazás tetején 3 oldal van: **Main**, **Server Settings**, **Currency**.

2. Menj a **Server Settings** oldalra és állítsd be a nyomtatót. A nyomtató típusától függően kövesd az A vagy a B opciót.

| Állapot | Kép |
|--------|-------|
| A nyomtató készen áll **NET/TCP és USB módban is** (A és **B** opció) | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/OK.JPEG" alt="Zebra nyomtató hálózati állapot" width="420" /> |
| A nyomtató nincs hálózatra csatlakoztatva — csak **USB módban** működik (B opció) | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/NO_NETWORK.JPEG" alt="Zebra nyomtató hálózati állapot – nincs kapcsolat" width="420" /> |

### A opció: NET/TCP (hálózati nyomtató)

1. A **Print Mode** legyen `NET/TCP`.
2. Kattints a `Find Printers` gombra a hálózati Zebra nyomtatók kereséséhez.
3. Válaszd ki/írd be a nyomtató IP címét (és a portot, általában `9100`).
4. Kattints a `Test Printer` gombra.
5. Kattints a `Save Configuration` gombra (alul).
6. Megjelenik egy felugró ablak, hogy a konfiguráció sikeresen mentve. Kattints az OK gombra a bezáráshoz. A szerver automatikusan újraindul.

### B opció: USB (helyi USB nyomtató)

1. A **Print Mode** legyen `USB`.
2. Válaszd ki a Zebra nyomtatót a legördülő listából.
3. Ha nem látod, kattints a `Refresh` gombra.
4. Kattints a `Test Printer` gombra.
5. Kattints a `Save Configuration` gombra (alul).
6. Megjelenik egy felugró ablak, hogy a konfiguráció sikeresen mentve. Kattints az OK gombra a bezáráshoz. A szerver automatikusan újraindul.

### Pénznem

1. Menj a **Currency** oldalra.
2. Válaszd ki a pénznemet, az árjavaslat típusát és a tizedeseket. (Az alapértelmezett beállítások Magyarországhoz vannak.)
3. Kattints a `Save Configuration` gombra (alul).

### Nyomtatás indítása

1. Menj a **Main** oldalra.
2. Kattints a `Start Server` gombra (ha nem indult el automatikusan).
3. Kattints az `Open Printer Page` gombra. (Ha Windows Explorer-ben nyílik meg, másold ki a linket és nyisd meg Chrome-ban vagy más böngészőben.)
4. Tipp: Mentsd el a webes felület linkjét könyvjelzőként.

### Az első címke nyomtatása

1. A webes felületen válaszd ki az ár módot: „SALE PRICE” vagy „NORMAL PRICE”.
2. Add meg az árat a javaslat gombokkal vagy kézzel beírva.
3. a) „SALE PRICE” mód: add meg a régi árat, válassz kedvezményt (20%–70%), vagy adj meg egy egyedi új árat.
   b) „NORMAL PRICE” mód: csak add meg az árat.
4. Állítsd be a nyomtatandó címkék mennyiségét (alapértelmezés szerint 1, ha nincs megadva).
5. Kattints a `Submit` gombra a címke nyomtatásához.
6. Ellenőrizd, hogy a címke megfelelően kinyomtatódott a Zebra nyomtatón.

**Gratulálunk!** Sikeresen telepítetted és beállítottad a Zebra Label Printer alkalmazást. Mostantól hatékonyan nyomtathatsz ár címkéket a webes felületen keresztül.

(Példa oldalak az alkalmazásban)

| Oldal | Kép |
|------|-----|
| Main | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_1.png" alt="Zebra Label Printer - Main" width="520" /> |
| Server Settings | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_2.png" alt="Zebra Label Printer - Server Settings" width="520" /> |
| Currency | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_3.png" alt="Zebra Label Printer - Currency" width="520" /> |
| Web Interface | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SCREENSHOT.png" alt="Zebra Label Printer Web Interface" width="520" /> |

**Megjegyzések:**
- Ha bármilyen problémát tapasztalsz a telepítés vagy beállítás során, nézd meg a README.md hibaelhárítás részét, vagy vedd fel a kapcsolatot a támogatással.
- Ha a telepítésnél az alapértelmezett beállításokat hagytad, az alkalmazás létrehoz egy asztali ikont, és a Windowszal együtt indul. (Elég az `Open Printer Page` gombra kattintani a használat elkezdéséhez.)
- A webes felület hivatkozását elmentheted könyvjelzőként a böngészőben.

**Ha hálózati problémát tapasztalsz NET/TCP módban, ellenőrizd az alábbiakat:**

Győződj meg róla, hogy az Ethernet kábel be van dugva a nyomtató alábbi portjába, és a nyomtató ugyanazon a hálózaton van, mint a PC:

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/CABLE.png" alt="Zebra nyomtató Ethernet port" width="420" />


### Köszönjük, hogy a Zebra Label Printer-t használod! Jó címkézést!
### Made with love by Marcell Tihanyi from Arena Mall Benetton