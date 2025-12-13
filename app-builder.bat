pyinstaller --name "zlp-updater" ^
    --onefile ^
    --windowed ^
    --icon=icon.png ^
    --add-data "static;static" ^
    --version-file=version.txt ^
    zlp-updater.py

pyinstaller --name "zlp-installer" ^
    --onefile ^
    --windowed ^
    --icon=icon.png ^
    --add-data "static;static" ^
    --version-file=version.txt ^
    zlp-installer.py

pyinstaller --name "zlp-uninstaller" ^
    --onefile ^
    --windowed ^
    --icon=icon.png ^
    --add-data "static;static" ^
    --version-file=version.txt ^
    zlp-uninstaller.py

pyinstaller --name "zlp-server" ^
    --onefile ^
    --windowed ^
    --icon=icon.png ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --version-file=version.txt ^
    zlp-server.py

pyinstaller --name "Zebra-Label-Printer" ^
    --onefile ^
    --windowed ^
    --icon=icon.png ^
    --add-data "static;static" ^
    --version-file=version.txt ^
    zlp-gui.py

rmdir /Q /s build
rmdir /Q /s __pycache__
rmdir /Q /s distribution
mkdir distribution
cd ./dist
move *.exe ..\distribution\
cd ..\
rmdir /Q /s dist
del /Q *.spec

