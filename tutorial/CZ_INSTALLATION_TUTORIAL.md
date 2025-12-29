# Návod k instalaci

## Kroky instalace

0. Požadavky:
   - Pro nejlepší zkušenost použijte Google Chrome.

1. Stáhněte si nejnovější verzi `zlp-installer.exe` ze stránky vydání. Jak je zobrazeno na obrázku níže. (Klikněte na tlačítko níže pro přechod na stránku stažení):
    
   [https://github.com/TMarccci/Zebra-Label-Printer/releases/latest](https://github.com/TMarccci/Zebra-Label-Printer/releases/latest)

   <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/FILE.png" alt="Stránka stažení" width="520" />

   | Při použití Microsoft Edge se může zobrazit upozornění jako toto: | Stačí postupovat podle pokynů „Keep“ a pokračovat ve stahování. |
   |---------------------------------------------------------------|--------------------------------------------------------------------------------|
   | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/EDGE_WARNING.png" alt="Upozornění Microsoft Edge" /> | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/EDGE_WARNING_2.png" alt="Microsoft Edge - Keep File"/> |

2. Spusťte aplikaci a potvrďte upozornění Windows SmartScreen, pokud se zobrazí.

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SMART_SCREEN_ACCEPT.png" alt="Upozornění Windows SmartScreen" width="520" />

3. Postupujte podle pokynů na obrazovce.
4. Dokončete průvodce instalací (nebojte se, pokud to trvá trochu déle — je to normální. Dejte si kávu ☕, než se to dokončí. 😉)

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/INSTALLER.png" alt="Průvodce instalací Zebra Label Printer" width="300" />

## První konfigurace

1. Otevřete `Zebra Label Printer.exe` (pokud se po instalaci nespustil automaticky).

Aplikace má nahoře 3 stránky: **Main**, **Server Settings**, **Currency**.

2. Přejděte na **Server Settings** a nastavte tiskárnu. Podle typu tiskárny postupujte podle Varianty A nebo Varianty B.

| Stav | Obrázek |
|--------|-------|
| Tiskárna je připravena **pro NET/TCP i USB režim** (Varianta A i **B**) | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/OK.JPEG" alt="Stav sítě tiskárny Zebra" width="420" /> |
| Tiskárna není připojena k síti — funguje pouze v **USB režimu** (Varianta B) | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/NO_NETWORK.JPEG" alt="Stav sítě tiskárny Zebra – nepřipojeno" width="420" /> |

### Varianta A: NET/TCP (síťová tiskárna)

1. Nastavte **Print Mode** na `NET/TCP`.
2. Klikněte na `Find Printers` pro vyhledání Zebra tiskáren v síti.
3. Vyberte/zadejte IP adresu tiskárny (a port, obvykle `9100`).
4. Klikněte na `Test Printer`.
5. Klikněte na `Save Configuration` (dole).
6. Zobrazí se okno potvrzující úspěšné uložení konfigurace. Klikněte na OK pro zavření. Server se automaticky restartuje.

### Varianta B: USB (lokální USB tiskárna)

1. Nastavte **Print Mode** na `USB`.
2. Vyberte Zebra tiskárnu z rozbalovacího seznamu.
3. Pokud ji nevidíte, klikněte na `Refresh`.
4. Klikněte na `Test Printer`.
5. Klikněte na `Save Configuration` (dole).
6. Zobrazí se okno potvrzující úspěšné uložení konfigurace. Klikněte na OK pro zavření. Server se automaticky restartuje.

### Měna

1. Přejděte na **Currency**.
2. Vyberte měnu, typ návrhů cen a desetinná místa. (Výchozí nastavení je pro Maďarsko.)
3. Klikněte na `Save Configuration` (dole).

### Začněte tisknout

1. Přejděte na **Main**.
2. Klikněte na `Start Server` (pokud se nespustil automaticky).
3. Klikněte na `Open Printer Page`. (Pokud se otevře ve Windows Exploreru, zkopírujte odkaz a otevřete jej v Chrome nebo jiném prohlížeči.)
4. Tip: Uložte si odkaz na webové rozhraní jako záložku v prohlížeči.

### Tisk první etikety

1. Ve webovém rozhraní vyberte režim ceny: „SALE PRICE“ nebo „NORMAL PRICE“.
2. Zadejte cenu pomocí tlačítek s návrhy nebo ručně.
3. a) Pro režim „SALE PRICE“: zadejte starou cenu, vyberte slevu (20%–70%) nebo zadejte vlastní novou cenu.
   b) Pro režim „NORMAL PRICE“: zadejte cenu přímo.
4. Nastavte množství etiket k tisku (výchozí je 1, pokud není zadáno).
5. Klikněte na `Submit` pro tisk etikety.
6. Ověřte, že se etiketa správně vytiskla na tiskárně Zebra.

**Gratulujeme!** Úspěšně jste nainstalovali a nakonfigurovali aplikaci Zebra Label Printer. Nyní můžete efektivně tisknout cenové etikety pomocí webového rozhraní.

(Ukázka stránek v aplikaci)

| Stránka | Obrázek |
|------|-------|
| Main | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_1.png" alt="Zebra Label Printer - Main" width="520" /> |
| Server Settings | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_2.png" alt="Zebra Label Printer - Server Settings" width="520" /> |
| Currency | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_3.png" alt="Zebra Label Printer - Currency" width="520" /> |
| Web Interface | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SCREENSHOT.png" alt="Zebra Label Printer Web Interface" width="520" /> |

**Poznámky:**
- Pokud narazíte na problémy během instalace nebo konfigurace, podívejte se do části Řešení problémů v souboru README.md nebo kontaktujte podporu.
- Pokud jste během instalace ponechali výchozí nastavení, aplikace vytvoří ikonu na ploše a bude se spouštět spolu s Windows. (Pro zahájení práce stačí kliknout na `Open Printer Page`.)
- Odkaz na webové rozhraní si můžete uložit jako záložku v prohlížeči.

**Pokud máte potíže s připojením k síti v režimu NET/TCP, ověřte následující:**

Ujistěte se, že je ethernetový kabel připojen do portu tiskárny níže a že tiskárna je ve stejné síti jako PC:

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/CABLE.png" alt="Ethernetový port tiskárny Zebra" width="420" />


### Děkujeme, že používáte Zebra Label Printer! Přejeme příjemné štítkování!
### Made with love by Marcell Tihanyi from Arena Mall Benetton