
# Installation Tutorial

## Preparation

Before installing the Zebra Label Printer application, ensure your store meets the compatibility requirements.
Check if your zebra is on the network by clicking the X button on the printer. 
If the ethernet icon is green then your printer is connected to the network.


| Status | Image |
|--------|-------|
| Printer is okay | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/OK.JPEG" alt="Zebra Printer Network Status" width="420" /> |
| Printer is not okay | <img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/NO_NETWORK.JPEG" alt="Zebra Printer Network Status Not OK" width="420" /> |

**If you encounter issues with network connectivity, ensure the following:**

Make sure you have an ethernet cable connected to your printer in the port below:

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/CABLE.png" alt="Zebra Printer Ethernet Port" width="420" />

## Installation Steps

1. Download the latest version of `zlp-installer.exe` from the releases page. (Click on the button below to navigate to the download page.)

    [Download zlp-installer.exe](https://github.com/TMarccci/Zebra-Label-Printer/releases/latest)

2. Launch the Application and Accept Windows SmartScreen warning if it appears.

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SMART_SCREEN_ACCEPT.png" alt="Windows SmartScreen Warning" width="520" />

3. Follow the on-screen prompts
4. Complete the setup wizard ( Don't worry if it takes a bit longer, it's normal. Grab a coffee ☕ while you wait. 😉 )

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/INSTALLER.png" alt="Zebra Label Printer Setup Wizard" width="520" />

5. Launch the application from the Desktop icon or Start Menu. (If it doesn't open automatically after installation.)

## First Time Configuration

1. Open `Zebra Label Printer.exe`. if not opened automatically after installation.
2. In the configuration window, click on `Find Printers` to scan your network for Zebra printers.
3. Select your printer from the list. You can try to print a test label to confirm it is your printer.
4. If your printer is not found, manually enter the IP address and port (usually `9100`).
5. Choose your currency, price suggestions, and decimal settings depending on your store's requirements.
6. Save the settings.
7. Click `Start Server`. if not started automatically. 
8. To Open the web interface, click on `Open Web Interface` button.

(Example of the configuration window)

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SCREENSHOT.png" alt="Zebra Label Printer Configuration Window" width="620" />

---

**Notes:**
- If you encounter any issues during installation or configuration, refer to the Troubleshooting section in the README.md or contact support for assistance.
- If you kept the default settings during installation, the application will create a Desktop icon and it will Start with Windows for convenience. (You just have to press the `Open Web Interface` button to start using it.)
- You can save the Web Interface link as a bookmark in your browser for easy access.

## Printing Your First Label

1. In the web interface, select the price mode: "SALE PRICE" or "NORMAL PRICE".
2. Enter the price using the suggestion buttons or manually input the price.
3. Set the quantity of labels to print (default is 1, if not specified).
4. Click `Submit` to print the label.
5. Verify that the label prints correctly from your Zebra printer.

(Web Interface Screenshot)

<img src="https://raw.githubusercontent.com/TMarccci/Zebra-Label-Printer/refs/heads/main/tutorial/pictures/SCREENSHOT_2.png" alt="Zebra Label Printer Web Interface" />


**Congratulations!** You have successfully installed and configured the Zebra Label Printer application. You can now print price labels efficiently using the web interface.