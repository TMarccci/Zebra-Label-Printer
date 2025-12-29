
# Installation Tutorial

## Installation Steps

0. Prerequisites:
   - Use Google Chrome for the best experience.

1. Download the latest version of `zlp-installer.exe` from the releases page. As shown in the image below. (Click on the button below to navigate to the download page):
    
    [https://github.com/TMarccci/Zebra-Label-Printer/releases/latest](https://github.com/TMarccci/Zebra-Label-Printer/releases/latest)

    <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/FILE.png" alt="Download Page" width="520" />

    | When using Microsoft Edge, you might see a warning like this: | Just follow the "Keep" instructions to proceed with the download. |
    |---------------------------------------------------------------|--------------------------------------------------------------------------------|
    | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/EDGE_WARNING.png" alt="Microsoft Edge Warning" /> | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/EDGE_WARNING_2.png" alt="Microsoft Edge Keep File"/> |

2. Launch the Application and Accept Windows SmartScreen warning if it appears.

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SMART_SCREEN_ACCEPT.png" alt="Windows SmartScreen Warning" width="520" />

3. Follow the on-screen prompts
4. Complete the setup wizard ( Don't worry if it takes a bit longer, it's normal. Grab a coffee while you wait. :) )

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/INSTALLER.png" alt="Zebra Label Printer Setup Wizard" width="300" />

## First Time Configuration

1. Open `Zebra Label Printer.exe` (if it didn't open automatically after installation).

The app has 3 pages at the top: **Main**, **Server Settings**, **Currency**.

2. Go to **Server Settings** and configure your printer. According to your printer type, follow either Option A or Option B below.

| Status | Image |
|--------|-------|
| Printer is ready to **work with both NET/TCP and USB mode** (A and **B** option) | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/OK.JPEG" alt="Zebra Printer Network Status" width="420" /> |
| Printer is not connected to the network, it is only working with **USB mode** (B option) | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/NO_NETWORK.JPEG" alt="Zebra Printer Network Status Not OK" width="420" /> |

### Option A: NET/TCP (Network printer)

1. Set **Print Mode** to `NET/TCP`.
2. Click `Find Printers` to scan your network for Zebra printers.
3. Select/enter the printer IP (and port, usually `9100`).
4. Click `Test Printer`.
5. Click `Save Configuration` (at the bottom).
6. There will be a popup meaning the configuration was saved successfully. Click OK to close it. The server will restart automatically.

### Option B: USB (Local USB printer)

1. Set **Print Mode** to `USB`.
2. Select your Zebra printer from the dropdown.
3. If you don't see it, click `Refresh`.
4. Click `Test Printer`.
5. Click `Save Configuration` (at the bottom).
6. There will be a popup meaning the configuration was saved successfully. Click OK to close it. The server will restart automatically.

### Currency

1. Go to **Currency**.
2. Choose currency, price suggestion type, and decimals. (Default settings are for Hungary)
3. Click `Save Configuration` (at the bottom).

### Start printing

1. Go to **Main**.
2. Click `Start Server` (if it didn't start automatically).
3. Click `Open Printer Page`. (if it opens in Windows Explorer, copy the link and open it in Chrome or another browser)
4. Tip: Save the Web Interface link as a bookmark in your browser for easy access.

### Printing Your First Label

1. In the web interface, select the price mode: "SALE PRICE" or "NORMAL PRICE".
2. Enter the price using the suggestion buttons or manually input the price.
3. a) For "SALE PRICE" mode: Enter the old price, select a discount percentage (20%-70%) or enter a custom new price.
   b) For "NORMAL PRICE" mode: Just enter the price directly.
4. Set the quantity of labels to print (default is 1, if not specified).
5. Click `Submit` to print the label.
6. Verify that the label prints correctly from your Zebra printer.

**Congratulations!** You have successfully installed and configured the Zebra Label Printer application. You can now print price labels efficiently using the web interface.

(Example pages in the app)

| Page | Image |
|------|-------|
| Main | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_1.png" alt="Zebra Label Printer - Main page" width="520" /> |
| Server Settings | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_2.png" alt="Zebra Label Printer - Server Settings page" width="520" /> |
| Currency | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/APP_SCREENSHOT_3.png" alt="Zebra Label Printer - Currency page" width="520" /> |
| Web Interface | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SCREENSHOT.png" alt="Zebra Label Printer Web Interface" width="520" /> |

**Notes:**
- If you encounter any issues during installation or configuration, refer to the Troubleshooting section in the README.md or contact support for assistance.
- If you kept the default settings during installation, the application will create a Desktop icon and it will Start with Windows for convenience. (You just have to press the `Open Printer Page` button to start using it.)
- You can save the Web Interface link as a bookmark in your browser for easy access.

**If you encounter issues with network connectivity when using NET/TCP mode, ensure the following:**

Make sure you have an ethernet cable connected to your printer in the port below and the printer is connected to the same network as your PC.:

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/CABLE.png" alt="Zebra Printer Ethernet Port" width="420" />

### Thank you for using Zebra Label Printer! Happy labeling! 
### Made with love by Marcell Tihanyi from Arena Mall Benetton