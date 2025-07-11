# Generating Light Stimulus for experiments

This folder contains an Arduino sketch (`stimulus_light.ino`) for controlling an RGB LED using both a push button and serial commands. The code supports smooth debouncing of the button using the Bounce2 library and allows dynamic color control via the serial interface.

## Usage
1. Open `stimulus_light.ino` in the Arduino IDE.
2. Connect your hardware as described above.
3. Select your Arduino board and port from **Tools > Board** and **Tools > Port**.
4. Upload the sketch to your Arduino.
5. Open the Serial Monitor by clicking the magnifying glass icon in the top right of the Arduino IDE, or go to **Tools > Serial Monitor**. Set the baud rate to 9600.
6. To change the LED color, type a command like `255,0,0` (for red) and press Enter.
7. Press the button to toggle the LED on or off. The current state will be shown in the Serial Monitor.

### Serial Command Format
- Send `R,G,B` values (0–255) via the Serial Monitor to set the LED color.
- Example: `0,255,128` sets the LED to a teal color.


## Hardware Requirements
- Arduino Uno
- RGB LED strip
- 3 transistors
- Push button
- Breadboard and jumper wires

### Pin Connections
- Red LED: Pin 11
- Green LED: Pin 10
- Blue LED: Pin 9
- Button: Pin 2 (uses internal pull-up resistor)

## Library Dependencies
This sketch requires the [Bounce2](https://github.com/thomasfredericks/Bounce2) library for button debouncing.

### Installing Bounce2
1. Open the Arduino IDE.
2. Go to **Sketch > Include Library > Manage Libraries...**
3. In the Library Manager, search for `Bounce2`.
4. Click **Install**.

## Notes
- The button uses the internal pull-up resistor.
- The sketch prints status messages to the Serial Monitor for both button and serial actions.

