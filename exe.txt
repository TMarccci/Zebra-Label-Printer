pyinstaller --name "zebra-server" ^
    --onefile ^
    --windowed ^
    --icon=icon.png ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    zebra-server.py


pyinstaller --name "Zebra Label Printer" ^
    --onefile ^
    --windowed ^
    --icon=icon.png ^
    --add-binary "./dist/zebra-server.exe;." ^
    --add-data "static;static" ^
    gui.py
