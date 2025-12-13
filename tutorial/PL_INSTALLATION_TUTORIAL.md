# Poradnik instalacji

## Przygotowanie

Przed instalacją aplikacji Zebra Label Printer upewnij się, że sklep spełnia wymagania kompatybilności.
Sprawdź, czy drukarka Zebra jest w sieci: naciśnij przycisk X na drukarce. Jeśli ikona Ethernet jest zielona, drukarka jest podłączona do sieci.

| Status | Obraz |
|--------|-------|
| Drukarka jest podłączona | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/OK.JPEG" alt="Status sieci drukarki Zebra" width="420" /> |
| Drukarka nie jest podłączona | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/NO_NETWORK.JPEG" alt="Status sieci drukarki Zebra – brak połączenia" width="420" /> |

**Jeśli występują problemy z siecią, upewnij się, że:**

Przewód Ethernet jest podłączony do portu drukarki:

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/CABLE.png" alt="Port Ethernet drukarki Zebra" width="420" />

## Kroki instalacji

1. Pobierz najnowszą wersję `zlp-installer.exe` ze strony wydań. (Kliknij poniższy link, aby przejść do strony pobierania.)

    [Pobierz zlp-installer.exe](https://github.com/TMarccci/Zebra-Label-Printer/releases/latest)

2. Uruchom instalator i zaakceptuj ostrzeżenie Windows SmartScreen, jeśli się pojawi.

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SMART_SCREEN_ACCEPT.png" alt="Ostrzeżenie Windows SmartScreen" width="520" />

3. Postępuj zgodnie z instrukcjami na ekranie.
4. Zakończ kreator instalacji (to normalne, że może chwilę potrwać — możesz zrobić sobie kawę ☕).

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/INSTALLER.png" alt="Kreator instalacji Zebra Label Printer" width="520" />

5. Uruchom aplikację z ikony na pulpicie lub z Menu Start. (Jeśli nie otworzyła się automatycznie po instalacji.)

## Pierwsza konfiguracja

1. Otwórz `Zebra Label Printer.exe` (jeśli nie uruchomiło się automatycznie po instalacji).
2. W oknie konfiguracji kliknij `Find Printers`, aby zeskanować sieć w poszukiwaniu drukarek Zebra.
3. Wybierz swoją drukarkę z listy. Możesz wykonać wydruk testowy, aby upewnić się, że to właściwe urządzenie.
4. Jeśli drukarka nie została znaleziona, wpisz ręcznie adres IP i port (zwykle `9100`).
5. Wybierz walutę, sugestie cen oraz ustawienia miejsc po przecinku zgodnie z wymaganiami sklepu.
6. Zapisz ustawienia.
7. Kliknij `Start Server` (jeśli nie został uruchomiony automatycznie).
8. Aby otworzyć interfejs WWW, kliknij przycisk `Open Web Interface`.

(Przykład okna konfiguracji)

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SCREENSHOT.png" alt="Okno konfiguracji Zebra Label Printer" width="620" />

---

**Uwagi:**
- Jeśli napotkasz problemy podczas instalacji lub konfiguracji, zajrzyj do sekcji Rozwiązywanie problemów w README.md lub skontaktuj się z pomocą techniczną.
- Jeśli pozostawiłeś domyślne ustawienia podczas instalacji, aplikacja utworzy ikonę na pulpicie i będzie uruchamiana wraz z systemem Windows. (Wystarczy kliknąć `Open Web Interface`, aby rozpocząć korzystanie.)
- Możesz zapisać link do interfejsu WWW jako zakładkę w przeglądarce.

## Wydruk pierwszej etykiety

1. W interfejsie WWW wybierz tryb ceny: „SALE PRICE” (cena promocyjna) lub „NORMAL PRICE” (cena regularna).
2. Wprowadź cenę, używając przycisków z sugestiami lub wpisz cenę ręcznie.
3. Ustaw liczbę etykiet do wydruku (domyślnie 1, jeśli nie określono).
4. Kliknij `Submit`, aby wydrukować etykietę.
5. Sprawdź, czy etykieta poprawnie wydrukowała się na drukarce Zebra.

(Web Interface Screenshot)

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SCREENSHOT_2.png" alt="Zebra Label Printer interfejs WWW" />


**Gratulacje!** Pomyślnie zainstalowałeś i skonfigurowałeś aplikację Zebra Label Printer. Teraz możesz efektywnie drukować etykiety cenowe za pomocą interfejsu WWW.