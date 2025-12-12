
# Zebra Label Printer

Zebra Label Printer is a Windows desktop app to print clean retail price labels on Zebra network printers. It supports normal and sale price workflows, quantity management, and QR access to the local web server.

## Features

- **Dual Price Modes**: Switch between sale price (with discount) and normal price labels
- **Discount Calculator**: Quick discount buttons (20%-70%) or manual entry
- **Print History**: Recent prints stored locally for quick reprinting
- **Price Suggestions**: Pre-configured price tables for Hungary, Poland, and Czech markets
- **Multi-language Currency**: Configurable currency display (HUF, CZK, PLN, etc.)
- **Decimal Support**: Optional decimal place display with configuration
- **QR Code**: Generate QR codes for easy network access

## Quick Start

1. Download the latest release ZIP from the project Releases page.
2. Run `zlp-installer.exe` (or `zlp-installer.py` if using Python) and follow the steps.
3. After installation, open `Zebra Label Printer.exe`.
4. Enter your printer's IP address and port (usually `9100`). You can use Find Printers to scan your networks.
5. Save the settings.
6. Click `Start Server`. The app shows a QR code and web link.
7. Print your first label using the GUI or the web interface.

Tip: Create a Desktop icon and enable Start with Windows during install for convenience.

## Installation

### Requirements
- Windows 10 or later
- Zebra network printer (configured with IP and port)

### Find Your Printer IP
- On the Zebra printer, print a network configuration label (usually via the printer menu). Look for `IP Address`.
- Or check your router's connected devices list for the printer.
- The default port is `9100` for most Zebra network printers.

### Setup

1. Download the latest release.
2. Run `zlp-installer.exe` and select your preferences.
3. Launch `Zebra Label Printer.exe`.
4. Configure Printer IP and Port, Currency, Price Suggestions, and Decimals.
5. Click `Start Server` to enable the local web interface.

### Uninstallation

- Run `zlp-uninstaller.exe`.
- Select which items to remove (app files, Desktop shortcut, Startup shortcut).
- Confirm to proceed. The tool stops running processes, removes shortcuts, and deletes the app folder at `APP_FOLDER`.

Manual removal alternative:
- Close the app and updater.
- Delete the app folder in `C:\Users\<YourUsername>\Zebra Label Printer`.
- Remove `Zebra Label Printer.lnk` from your Desktop and from `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`.

## Usage

### Basic Workflow

1. **Select Price Mode**: Choose "SALE PRICE" or "NORMAL PRICE"
2. **Enter Price**: Click a suggestion button or manually enter the price
3. **Set Quantity**: Use quick buttons or enter manually (default: 1). If not given, prints one label.
4. **Print**: Click `Submit` to print the label

### Sale Price Mode

1. Enter the old price
2. Select a discount percentage (20%-70%) or enter a custom new price
3. Set quantity (or leave empty to print one) and submit

### Sale Price Mode with custom percentage
1. Enter the old price
2. Enter the desired new price
3. Set quantity (or leave empty to print one) and submit

### Normal Price Mode

1. Enter the price
2. Set quantity (or leave empty to print one) and submit

### How to use on Mobile Devices

1. Enable Wi-Fi hotspot on your PC or connect both PC and mobile to the same network.
2. Open the Zebra Label Printer app on your PC and start the server.
3. Scan the QR code or enter the displayed URL in your mobile browser.
4. Use the web interface to print labels directly from your mobile device.

### Test Printer
- Use the `Test Printer` button in the GUI to send a small test page. If it prints, your IP/port are correct.

## Configuration

Edit settings in the GUI:

- **Server Port**: Web interface port (default: 5000)
- **Printer IP**: Network address of your Zebra printer
- **Printer Port**: Usually 9100
- **Currency**: Display currency code
- **Price Suggestions**: Choose market type (Hungary/Poland/Czech)
- **Decimals**: Enable/disable decimal display

Settings are saved automatically to `~/Documents/Zebra Label Printer/gui_config.json`

Tip: The GUI shows an `Unsaved changes` indicator when you edit settings. Click `Save` to persist.

## Troubleshooting

- **No print output**: Verify the Zebra printer IP and that port `9100` is open. Try `Test Printer`.
- **Firewall blocks**: Allow `Zebra Label Printer.exe` and `zlp-server.exe` through Windows Firewall, or run as Administrator for the first start.
- **Printer offline**: Check network cable/Wi‑Fi and ping the printer IP.
- **Duplicate app instance**: The app prevents multiple instances. If you still see issues, close other instances or reboot.
- **Slow downloads in installer**: Progress bar and animated dots indicate activity; wait until the percentage reaches 100%.
- **Update available**: Use `Check for Updates` in the GUI. The updater can self-update.

## License

See LICENSE.txt for details.

## Acknowledgements
- Uses PyQt5 for the GUI
- Uses Flask for the server backend
- Uses qrcode for QR code generation
- Uses Pillow for image processing
- Uses requests for HTTP requests

## Support
For issues or feature requests, please contact the developer or open an issue on the project's repository.
Email: contact@tmarccci.hu
