# Návod k instalaci

## Příprava

Před instalací aplikace Zebra Label Printer se ujistěte, že vaše prodejna splňuje požadavky na kompatibilitu.
Zkontrolujte, zda je tiskárna Zebra v síti: stiskněte tlačítko X na tiskárně. Pokud je ikona Ethernet zelená, tiskárna je připojena k síti.

| Stav | Obrázek |
|------|---------|
| Tiskárna je připravena pracovat v režimu NET/TCP i USB | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/OK.JPEG" alt="Stav sítě tiskárny Zebra" width="420" /> |
| Tiskárna není připojena k síti — funguje pouze v režimu USB | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/NO_NETWORK.JPEG" alt="Stav sítě tiskárny Zebra – nepřipojeno" width="420" /> |

**Pokud máte potíže s připojením k síti, ověřte následující:**

Ujistěte se, že je ethernetový kabel připojen do portu tiskárny:

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/CABLE.png" alt="Ethernetový port tiskárny Zebra" width="420" />

## Kroky instalace

1. Stáhněte si nejnovější verzi `zlp-installer.exe` ze stránky vydání. (Klikněte na odkaz níže pro přechod na stránku stažení.)

    [Stáhnout zlp-installer.exe](https://github.com/TMarccci/Zebra-Label-Printer/releases/latest)

2. Spusťte instalátor a potvrďte upozornění Windows SmartScreen, pokud se zobrazí.

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SMART_SCREEN_ACCEPT.png" alt="Upozornění Windows SmartScreen" width="520" />

3. Postupujte podle pokynů na obrazovce.
4. Dokončete průvodce instalací (je normální, že to může chvíli trvat — klidně si dejte kávu ☕).

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/INSTALLER.png" alt="Průvodce instalací Zebra Label Printer" width="520" />

5. Spusťte aplikaci z ikony na ploše nebo z nabídky Start. (Pokud se po instalaci nespustila automaticky.)

## První konfigurace

V aplikaci jsou nahoře 3 stránky: **Main**, **Server Settings**, **Currency**.

1. Otevřete `Zebra Label Printer.exe` (pokud se po instalaci nespustil automaticky).
2. Přejděte na **Server Settings**.

### Varianta A: NET/TCP (síťová tiskárna)

1. Nastavte **Print Mode** na `NET/TCP`.
2. Klikněte na `Find Printers` pro vyhledání Zebra tiskáren v síti.
3. Vyberte/zadejte IP adresu tiskárny (a port, obvykle `9100`).
4. Klikněte na `Test Printer`.
5. Klikněte na `Save Configuration` (dole).

### Varianta B: USB (USB tiskárna připojená k PC)

1. Nastavte **Print Mode** na `USB`.
2. Vyberte Zebra tiskárnu z rozbalovacího seznamu.
3. Pokud ji nevidíte, klikněte na `Refresh`.
4. Klikněte na `Test Printer`.
5. Klikněte na `Save Configuration` (dole).

### Měna

1. Přejděte na **Currency**.
2. Nastavte měnu, typ návrhů cen a desetinná místa.
3. Klikněte na `Save Configuration` (dole).

### Začněte tisknout

1. Přejděte na **Main**.
2. Klikněte na `Start Server` (pokud se nespustil automaticky).
3. Klikněte na `Open Printer Page`.

(Ukázka stránek)

| Stránka | Obrázek |
|--------|---------|
| Main | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_1.png" alt="Zebra Label Printer - Main" width="520" /> |
| Server Settings | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_2.png" alt="Zebra Label Printer - Server Settings" width="520" /> |
| Currency | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_3.png" alt="Zebra Label Printer - Currency" width="520" /> |

---

**Poznámky:**
- Pokud narazíte na problémy během instalace nebo konfigurace, podívejte se do části Řešení problémů v souboru README.md nebo kontaktujte podporu.
- Pokud jste během instalace ponechali výchozí nastavení, aplikace vytvoří ikonu na ploše a bude se spouštět spolu s Windows. (Pro zahájení práce stačí kliknout na `Open Printer Page`.)
- Odkaz na webové rozhraní si můžete uložit jako záložku v prohlížeči.

Tip: Pokud chcete přejít na jinou stránku bez uložení, aplikace se zeptá: Save / Discard / Cancel.

## Vytisknutí první etikety

1. Ve webovém rozhraní zvolte režim ceny: „SALE PRICE“ (akční cena) nebo „NORMAL PRICE“ (běžná cena).
2. Zadejte cenu pomocí tlačítek s návrhy nebo ručně.
3. Nastavte množství etiket k tisku (výchozí je 1, pokud není zadáno).
4. Klikněte na `Submit` pro tisk etikety.
5. Ověřte, že se etiketa správně vytiskla na tiskárně Zebra.

(Web Interface Screenshot)

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SCREENSHOT.png" alt="Webové rozhraní Zebra Label Printer" />


**Gratulujeme!** Úspěšně jste nainstalovali a nakonfigurovali aplikaci Zebra Label Printer. Nyní můžete efektivně tisknout cenové etikety pomocí webového rozhraní.