# Tardigrade-KITP2025

Code and documentation related to the Tardigrade project in KITP QBio 2025.

## Software installation

### SpinView (Camera Interface)

We will be using [SpinView](https://softwareservices.flir.com/Spinnaker/latest/_spin_view_guide.html) to record videos from the microscope.

To use [SpinView](https://softwareservices.flir.com/Spinnaker/latest/_spin_view_guide.html), you will need to install the [Spinnaker SDK](https://flir.custhelp.com/app/answers/detail/a_id/4327/~/flir-spinnaker-sdk---getting-started-with-the-spinnaker-sdk). Below are the instructions for installing the Spinnaker SDK and SpinView for Windows and macOS:

#### Windows

1. Download the latest Spinnaker SDK for Windows from [here](https://www.teledynevisionsolutions.com/support/support-center/software-firmware-downloads/iis/spinnaker-sdk-download/spinnaker-sdk--download-files/?pn=Spinnaker+SDK&vn=Spinnaker+SDK).
2. Run the installer and follow the on-screen instructions.
3. Select the USB-3 related drivers for your camera during installation.
4. Reboot your computer if prompted.
5. Open SpinView (if not found via search, go to `C:\Program Files\FLIR Systems\Spinnaker\bin64\vs2015\SpinView_WPF.exe`).
6. Connect your camera and test SpinView.

#### macOS

1. Install dependencies using Homebrew ([detailed instructions](https://www.teledynevisionsolutions.com/support/support-center/application-note/iis/getting-started-with-spinnaker-sdk-on-macos/)):
    - Install [Homebrew](https://brew.sh/): Open Terminal and enter:
      ```fish
      /bin/bash -c "(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```
    - Install dependencies: Open Terminal and enter:
      ```fish
      brew install pkg-config libomp libusb ffmpeg@2.8
      ```
2. Download the Spinnaker SDK for macOS from [here](https://www.teledynevisionsolutions.com/support/support-center/software-firmware-downloads/iis/spinnaker-sdk-download/spinnaker-sdk--download-files/?pn=Spinnaker+SDK&vn=Spinnaker+SDK). Download version 4.1 for Apple Silicon Macs (M1 and above), or version 3.2 for Intel-based Macs.
3. Unpack the zip file, open the downloaded `.dmg`, and run the `.pkg` installer. If you see a warning that "Apple could not verify Spinnaker.pkg," go to System Settings → Privacy & Security, and allow the package to open by clicking "Open Anyway." Then follow the installation instructions.
4. Open SpinView (located at `/Applications/Spinnaker/apps/SpinView_QT`).
5. Connect your camera and test SpinView.

### Arduino IDE (Stimulus Control)

We will use Arduino for stimulus control. To use the code in this repository, it is recommended to install the Arduino IDE.

#### Windows

1. Download the latest Arduino IDE for Windows from the [official Arduino website](https://www.arduino.cc/en/software).
2. Run the downloaded installer and follow the on-screen instructions.
3. During installation, allow the installer to install drivers if prompted.
4. Once installed, launch the Arduino IDE and connect your Arduino board to verify the installation.

#### macOS

If you have already installed Homebrew (see the SpinView step above), you can easily install the Arduino IDE by entering the following in the terminal:
```fish
brew install arduino-ide
```

Alternatively, you can install the Arduino IDE by:
1. Downloading the latest Arduino IDE for macOS from the [official Arduino website](https://www.arduino.cc/en/software).
2. Opening the downloaded `.dmg` file and dragging the Arduino application to your `Applications` folder.
3. Launching the Arduino IDE. If you see a security warning, go to System Settings → Privacy & Security and allow the app to open.
4. Connecting your Arduino board and verifying that it appears under Tools → Port in the IDE.

