# Tardigrade-KITP2025

Code and documentation related to the Tardigrade project in KITP QBio 2025.

## Software installation (on Mac) 
1)      Install Anaconda (will install Python 3) 

2)	Download and install Visual Studio Code
   
3)	Download the Tardigrade Tracker Software from GitHub and save it to your desktop.
	a.	The file should contain the following. 
		i.	TardigradeTracker.YAML
		ii.	TardigradeTracker.py 
		iii.	TrajectoryTracker.py 
	b.	Download Test Videos and place them in the same directory as the code.
		https://drive.google.com/drive/folders/1HrRn6jHbMnu1ERJOPAouhAAELKpub8LO?usp=sharing
5)	Create a clean virtual environment for TardigradeTracker using the following code in terminal. 
		$$ conda env create -f TardigradeTracker.yaml
6)	 Check the environment creation using the following line.  
	 	$$ conda env list 
7)	 Activate the environment for TardigradeTracker using the following line of code 
   		$$ conda activate TardigradeTracker
8)	 Check that the environment has been properly established 
   		$$ conda list
The result should look like this 
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

8)	 Open VisualStudio code and open the TardigradeTracker.py file.

9)	 Click the run arrow in the upper right-hand corner
	 
10)	The code will begin to run, and a finder window will open – select the folder which contains the test videos and click on one of the video files.
    
12)	The video will load into the GUI, and you can begin your analysis.
	
13)	Click the video to select a box surrounding the tardigrade (draw the box big enough so the tardigrade never leaves the box throughout the video)
	
14)	Next ascertain that the tardigrade is circled throughout the video duration by the algorithm 
	a.	You can adjust contrast, brightness, and threshold to get the best fit

17)	 When you are satisfied that the tardigrade is tracked throughout the video hit the run button on the bottom of the GUI.

18)	This will generate two new files in the TardigradeTraker folder: a video showing the circled tardigrade and a CSV file containing extracted measurements. – to monitor progress, click to your Visual Studio Code where there is a percent readout. 


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
4. Once installed, follow the post installation steps below.

#### macOS

If you have already installed Homebrew (see the SpinView step above), you can easily install the Arduino IDE by entering the following in the terminal:
```fish
brew install arduino-ide
```

Alternatively, you can install the Arduino IDE by:
1. Downloading the latest Arduino IDE for macOS from the [official Arduino website](https://www.arduino.cc/en/software).
2. Opening the downloaded `.dmg` file and dragging the Arduino application to your `Applications` folder.
3. Once installed, follow the post installation steps below. If you see a security warning, go to System Settings → Privacy & Security and allow the app to open.

#### Post installation

To verify your Arduino IDE installation and board connection, follow these steps:

1. Open the Arduino IDE.
2. Go to **File > Examples > 01.Basics > Blink** to open the Blink example sketch.
3. Connect your Arduino board to your computer via USB.
4. Select the correct board type:
    - Go to **Tools > Board > Arduino AVR Boards > Arduino Uno** (or select your specific board model).
5. Select the correct port:
    - Go to **Tools > Port** and choose the port that corresponds to your connected Arduino.
6. In the Blink sketch, change both `delay(1000);` lines to `delay(100);` to make the LED blink faster.
7. Click the **Upload** button (right arrow icon) to upload the sketch to your Arduino.
8. Observe the onboard LED (usually labeled "L" on the Arduino Uno). It should now blink rapidly, confirming that your setup is working correctly.
