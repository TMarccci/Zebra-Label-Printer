# Poradnik instalacji

## Kroki instalacji

0. Wymagania:
   - Dla najlepszych efektów użyj Google Chrome.

1. Pobierz najnowszą wersję `zlp-installer.exe` ze strony wydań. Jak pokazano na obrazku poniżej. (Kliknij przycisk poniżej, aby przejść do strony pobierania):
    
   [https://github.com/TMarccci/Zebra-Label-Printer/releases/latest](https://github.com/TMarccci/Zebra-Label-Printer/releases/latest)

   <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/FILE.png" alt="Strona pobierania" width="520" />

   | Jeśli używasz Microsoft Edge, możesz zobaczyć ostrzeżenie jak poniżej: | Wystarczy wykonać instrukcje „Keep”, aby kontynuować pobieranie. |
   |---------------------------------------------------------------|--------------------------------------------------------------------------------|
   | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/EDGE_WARNING.png" alt="Ostrzeżenie Microsoft Edge" /> | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/EDGE_WARNING_2.png" alt="Microsoft Edge - Keep File"/> |

2. Uruchom aplikację i zaakceptuj ostrzeżenie Windows SmartScreen, jeśli się pojawi.

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SMART_SCREEN_ACCEPT.png" alt="Ostrzeżenie Windows SmartScreen" width="520" />

3. Postępuj zgodnie z instrukcjami na ekranie.
4. Zakończ kreator instalacji (nie martw się, jeśli potrwa trochę dłużej — to normalne. Zrób sobie kawę ☕, zanim skończy. 😉)

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/INSTALLER.png" alt="Kreator instalacji Zebra Label Printer" width="300" />

## Pierwsza konfiguracja

1. Otwórz `Zebra Label Printer.exe` (jeśli nie uruchomiło się automatycznie po instalacji).

Aplikacja ma 3 strony u góry: **Main**, **Server Settings**, **Currency**.

2. Przejdź do **Server Settings** i skonfiguruj drukarkę. W zależności od typu drukarki postępuj zgodnie z Opcją A lub Opcją B.

| Status | Obraz |
|--------|-------|
| Drukarka jest gotowa do pracy w trybie **NET/TCP i USB** (Opcja A i **B**) | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/OK.JPEG" alt="Status sieci drukarki Zebra" width="420" /> |
| Drukarka nie jest podłączona do sieci — działa tylko w trybie **USB** (Opcja B) | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/NO_NETWORK.JPEG" alt="Status sieci drukarki Zebra – brak połączenia" width="420" /> |

### Opcja A: NET/TCP (drukarka sieciowa)

1. Ustaw **Print Mode** na `NET/TCP`.
2. Kliknij `Find Printers`, aby przeskanować sieć w poszukiwaniu drukarek Zebra.
3. Wybierz/wpisz adres IP drukarki (i port, zwykle `9100`).
4. Kliknij `Test Printer`.
5. Kliknij `Save Configuration` (na dole).
6. Pojawi się okno potwierdzające zapis konfiguracji. Kliknij OK, aby je zamknąć. Serwer zrestartuje się automatycznie.

### Opcja B: USB (lokalna drukarka USB)

1. Ustaw **Print Mode** na `USB`.
2. Wybierz drukarkę Zebra z listy.
3. Jeśli jej nie widzisz, kliknij `Refresh`.
4. Kliknij `Test Printer`.
5. Kliknij `Save Configuration` (na dole).
6. Pojawi się okno potwierdzające zapis konfiguracji. Kliknij OK, aby je zamknąć. Serwer zrestartuje się automatycznie.

### Waluta

1. Przejdź do **Currency**.
2. Wybierz walutę, typ sugestii cen i liczbę miejsc po przecinku. (Domyślne ustawienia są dla Węgier.)
3. Kliknij `Save Configuration` (na dole).

### Start drukowania

1. Przejdź do **Main**.
2. Kliknij `Start Server` (jeśli nie uruchomił się automatycznie).
3. Kliknij `Open Printer Page`. (Jeśli otworzy się w Windows Explorer, skopiuj link i otwórz go w Chrome lub innej przeglądarce.)
4. Wskazówka: Zapisz link do interfejsu WWW jako zakładkę w przeglądarce.

### Drukowanie pierwszej etykiety

1. W interfejsie WWW wybierz tryb ceny: „SALE PRICE” lub „NORMAL PRICE”.
2. Wpisz cenę, używając przycisków z sugestiami lub wprowadzając ją ręcznie.
3. a) Dla trybu „SALE PRICE”: wpisz starą cenę, wybierz procent rabatu (20%–70%) lub wpisz własną nową cenę.
   b) Dla trybu „NORMAL PRICE”: po prostu wpisz cenę.
4. Ustaw liczbę etykiet do wydruku (domyślnie 1, jeśli nie określono).
5. Kliknij `Submit`, aby wydrukować etykietę.
6. Sprawdź, czy etykieta poprawnie wydrukowała się na drukarce Zebra.

**Gratulacje!** Udało się — aplikacja Zebra Label Printer jest zainstalowana i skonfigurowana. Teraz możesz drukować etykiety cenowe za pomocą interfejsu WWW.

(Przykładowe strony w aplikacji)

| Strona | Obraz |
|------|-------|
| Main | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_1.png" alt="Zebra Label Printer - Main" width="520" /> |
| Server Settings | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_2.png" alt="Zebra Label Printer - Server Settings" width="520" /> |
| Currency | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_3.png" alt="Zebra Label Printer - Currency" width="520" /> |
| Web Interface | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SCREENSHOT.png" alt="Zebra Label Printer Web Interface" width="520" /> |

**Uwagi:**
- Jeśli napotkasz problemy podczas instalacji lub konfiguracji, zajrzyj do sekcji Rozwiązywanie problemów w README.md lub skontaktuj się z pomocą techniczną.
- Jeśli pozostawiłeś domyślne ustawienia podczas instalacji, aplikacja utworzy ikonę na pulpicie i będzie uruchamiana wraz z systemem Windows. (Wystarczy kliknąć `Open Printer Page`, aby rozpocząć korzystanie.)
- Możesz zapisać link do interfejsu WWW jako zakładkę w przeglądarce.

**Jeśli masz problemy z łącznością sieciową w trybie NET/TCP, upewnij się, że:**

Upewnij się, że kabel Ethernet jest podłączony do portu drukarki poniżej, a drukarka jest w tej samej sieci co komputer:

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/CABLE.png" alt="Port Ethernet drukarki Zebra" width="420" />


### Dziękujemy za korzystanie z Zebra Label Printer! Miłego drukowania!
### Made with love by Marcell Tihanyi from Arena Mall Benetton