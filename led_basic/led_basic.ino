#include <Arduino.h>

#define RED_PIN 11    // Pin for red channel of RGB LED
#define GREEN_PIN 10  // Pin for green channel of RGB LED
#define BLUE_PIN 9    // Pin for blue channel of RGB LED
#define BUTTON_PIN 2  // Pin for button input

// Define brightness levels for each color channel (0-255)
int red_brightness = 255;
int green_brightness = 0;
int blue_brightness = 0;

// toggle related
int ledState = HIGH;        // the current state of the output pin
int buttonState = LOW;            // the current reading from the input pin
int lastButtonState = LOW;  // the previous reading from the input pin

// debounce parameters
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 100;    // the debounce time; increase if the output flickers

void setup() {
  // Set RGB pins as outputs
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  // Set the RGB LED to initial color (all off)
  analogWrite(RED_PIN, red_brightness);     // Set red brightness
  analogWrite(GREEN_PIN, green_brightness); // Set green brightness
  analogWrite(BLUE_PIN, blue_brightness);   // Set blue brightness

  // Begin serial communication for debugging and control
  Serial.begin(9600);
  Serial.println("Initialized RGB LEDs.");
}

void loop() {
  
  // Check for serial input to update LED brightness
  // Input format: R,G,B (e.g., 128,64,255)
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    // Parse input string for RGB values
    int comma1 = input.indexOf(',');
    int comma2 = input.lastIndexOf(',');
    if (comma1 > 0 && comma2 > comma1) {
      int r = input.substring(0, comma1).toInt();
      int g = input.substring(comma1 + 1, comma2).toInt();
      int b = input.substring(comma2 + 1).toInt();
      // Clamp values between 0 and 255
      red_brightness = constrain(r, 0, 255);
      green_brightness = constrain(g, 0, 255);
      blue_brightness = constrain(b, 0, 255);
      // Update brightness if LEDs are on
      if (ledState == HIGH) {
        analogWrite(RED_PIN, red_brightness);
        analogWrite(GREEN_PIN, green_brightness);
        analogWrite(BLUE_PIN, blue_brightness);
      }

      // Print confirmation to serial monitor
      Serial.print("Updated RGB to: ");
      Serial.print(red_brightness); Serial.print(", ");
      Serial.print(green_brightness); Serial.print(", ");
      Serial.println(blue_brightness);
    } else {
      // Print error if input format is invalid
      Serial.println("Invalid input. Use format: R,G,B");
    }
  }

  // Read the state of the button into a local variable:
  int reading = digitalRead(BUTTON_PIN);

  // If the button state has changed (due to noise or pressing):
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  // Only act if the button state has been stable for debounceDelay
// Only act if the button state has been stable for debounceDelay but less than 2*debounceDelay
if ((millis() - lastDebounceTime) > debounceDelay && (millis() - lastDebounceTime) < 2 * debounceDelay) {
    // If the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;
      // Only toggle the LED if the new button state is HIGH (button pressed)
      if (buttonState == HIGH) {
        ledState = !ledState;
        if (ledState == HIGH) {
          analogWrite(RED_PIN, red_brightness);
          analogWrite(GREEN_PIN, green_brightness);
          analogWrite(BLUE_PIN, blue_brightness);
        } else {
          analogWrite(RED_PIN, 0);
          analogWrite(GREEN_PIN, 0);
          analogWrite(BLUE_PIN, 0);
        }
      }
    }
  }
  // Save the reading for next loop iteration
  lastButtonState = reading;
}
