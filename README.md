
# Zebra Label Printer

A desktop application for printing price labels on Zebra printers with support for sale prices, normal prices, and quantity management.

## Features

- **Dual Price Modes**: Switch between sale price (with discount) and normal price labels
- **Discount Calculator**: Quick discount buttons (20%-70%) or manual entry
- **Print History**: Recent prints stored locally for quick reprinting
- **Price Suggestions**: Pre-configured price tables for Hungary, Poland, and Czech markets
- **Multi-language Currency**: Configurable currency display (HUF, CZK, PLN, etc.)
- **Decimal Support**: Optional decimal place display with configuration
- **QR Code**: Generate QR codes for easy network access

## Installation

### Requirements
- Windows 10 or later
- Zebra network printer (configured with IP and port)

### Find Your Printer IP
1. TODO: Add instructions to find printer IP

### Setup

1. Download the latest release
2. Extract the files to your preferred location
3. Run `Zebra Label Printer.exe` or the compiled `.exe`
4. Configure printer IP and port, currency, and other settings in the GUI
5. Click "Start Server" to begin

## Usage

### Basic Workflow

1. **Select Price Mode**: Choose "SALE PRICE" or "NORMAL PRICE"
2. **Enter Price**: Click a suggestion button or manually enter the price
3. **Set Quantity**: Use quick buttons or enter manually (default: 1). If not given, prints one label.
4. **Print**: Click "Submit" to print the label

### Sale Price Mode

1. Enter the old price
2. Select a discount percentage (20%-70%) or enter a custom new price
3. Set quantity (or no, to print one) and submit

### Sale Price Mode with custom percentage
1. Enter the old price
2. Enter the desired new price
3. Set quantity (or no, to print one) and submit

### Normal Price Mode

1. Enter the price
2. Set quantity (or no, to print one) and submit

## Configuration

Edit settings in the GUI:

- **Server Port**: Web interface port (default: 5000)
- **Printer IP**: Network address of your Zebra printer
- **Printer Port**: Usually 9100
- **Currency**: Display currency code
- **Price Suggestions**: Choose market type (Hungary/Poland/Czech)
- **Decimals**: Enable/disable decimal display

Settings are saved automatically to `~/Documents/Zebra Label Printer/gui_config.json`

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
