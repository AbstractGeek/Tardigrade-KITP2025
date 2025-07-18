# Tardigrade-KITP2025
Code and documentation related to the Tardigrade project in KITP QBio 2025.

## Experiments

### SpinView (Camera Interface)

We will be using [SpinView](https://softwareservices.flir.com/Spinnaker/latest/_spin_view_guide.html) to record videos from the microscope.

To use SpinView, you need to install the [Spinnaker SDK](https://flir.custhelp.com/app/answers/detail/a_id/4327/~/flir-spinnaker-sdk---getting-started-with-the-spinnaker-sdk). Instructions for Windows and macOS are below.

#### Windows

1. Download the latest Spinnaker SDK for Windows from [here](https://www.teledynevisionsolutions.com/support/support-center/software-firmware-downloads/iis/spinnaker-sdk-download/spinnaker-sdk--download-files/?pn=Spinnaker+SDK&vn=Spinnaker+SDK).
2. Run the installer and follow the on-screen instructions.
3. Select USB-3 drivers for your camera during installation.
4. Reboot if prompted.
5. Open SpinView (`C:\Program Files\FLIR Systems\Spinnaker\bin64\vs2015\SpinView_WPF.exe`).
6. Connect your camera and test SpinView.

#### macOS

1. Install dependencies using Homebrew ([instructions](https://www.teledynevisionsolutions.com/support/support-center/application-note/iis/getting-started-with-spinnaker-sdk-on-macos/)):
	- Install [Homebrew](https://brew.sh/):
	  ```sh
	  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	  ```
	- Install dependencies:
	  ```sh
	  brew install pkg-config libomp libusb ffmpeg@2.8
	  ```
2. Download the Spinnaker SDK for macOS from [here](https://www.teledynevisionsolutions.com/support/support-center/software-firmware-downloads/iis/spinnaker-sdk-download/spinnaker-sdk--download-files/?pn=Spinnaker+SDK&vn=Spinnaker+SDK). Use version 4.1 for Apple Silicon, or 3.2 for Intel Macs.
3. Unpack the zip, open the `.dmg`, and run the `.pkg` installer. If you see a security warning, allow the package in System Settings → Privacy & Security.
4. Open SpinView (`/Applications/Spinnaker/apps/SpinView_QT`).
5. Connect your camera and test SpinView.

### Arduino IDE (Stimulus Control)

We use Arduino for stimulus control. Install the Arduino IDE as follows:

#### Windows

1. Download the latest Arduino IDE from the [official website](https://www.arduino.cc/en/software).
2. Run the installer and follow instructions.
3. Allow driver installation if prompted.

#### macOS

If you have Homebrew, install Arduino IDE with:
```sh
brew install arduino-ide
```
Or download from the [official website](https://www.arduino.cc/en/software), open the `.dmg`, and drag Arduino to `Applications`. Allow the app in System Settings → Privacy & Security if needed.

#### Post Installation

1. Open Arduino IDE.
2. Go to **File > Examples > 01.Basics > Blink**.
3. Connect your Arduino board via USB.
4. Select the correct board (**Tools > Board > Arduino AVR Boards > Arduino Uno** or your model).
5. Select the correct port (**Tools > Port**).
6. In the Blink sketch, change both `delay(1000);` to `delay(100);`.
7. Click **Upload**.
8. The onboard LED should blink rapidly, confirming setup.

## TardigradeTracker

### Software Installation

1. Install Anaconda (Python 3).
2. Download and install Visual Studio Code.
3. Download the Tardigrade Tracker Software from GitHub and save to your desktop. The folder should contain:
	- `TardigradeTracker.yaml`
	- `TardigradeTracker.py`
	- `TrajectoryTracker.py`
	- [Test Videos](https://drive.google.com/drive/folders/1HrRn6jHbMnu1ERJOPAouhAAELKpub8LO?usp=sharing) (place in the same directory)
4. Create a clean virtual environment:
	```sh
	conda env create -f TardigradeTracker.yaml
	```
5. Check environment creation:
	```sh
	conda env list
	```
6. Activate the environment:
	```sh
	conda activate TardigradeTracker
	```
7. Verify environment:
	```sh
	conda list
	```
	The result should look like:
	```text
	# packages in environment at /path/to/anaconda3/envs/TardigradeTracker:
	#
	# Name                    Version                   Build  Channel
	bzip2                     1.0.8                h0d85af4_4    conda-forge
	ca-certificates           2025.1.31            h4653dfc_0    conda-forge
	libexpat                  2.7.0                h0dc2134_0    conda-forge
	libffi                    3.4.6                h9cdd2b7_0    conda-forge
	liblzma                   5.8.1                h9cdd2b7_0    conda-forge
	libzlib                   1.3.1                h9cdd2b7_0    conda-forge
	ncurses                   6.5                  h9cdd2b7_0    conda-forge
	openssl                   3.4.1                h0d85af4_0    conda-forge
	python                    3.13.2               h0d85af4_0    conda-forge
	readline                  8.2                  h8228510_1    conda-forge
	tk                        8.6.13               h9cdd2b7_1    conda-forge
	tzdata                    2025b                h0c530f3_0    conda-forge
	# pip packages:
	easygui                  0.98.3
	joblib                   1.4.2
	numpy                    2.2.4
	opencv-python            4.11.0.86
	pillow                   11.1.0
	scikit-learn             1.6.1
	scipy                    1.15.2
	threadpoolctl            3.6.0
	tqdm                     4.67.1
	```
8. Open Visual Studio Code and the `TardigradeTracker.py` file.
9. Click the run arrow in the upper right corner.
10. When prompted, select the folder containing test videos and choose a video file.
11. The video loads into the GUI for analysis.
12. Click the video to draw a box around the tardigrade (large enough so it stays inside throughout).
13. Ensure the algorithm tracks the tardigrade throughout the video. Adjust contrast, brightness, and threshold as needed.
14. When satisfied, click the run button at the bottom of the GUI.
15. Two new files are generated: a video showing the tracked tardigrade and a CSV with extracted measurements. Monitor progress in Visual Studio Code.
