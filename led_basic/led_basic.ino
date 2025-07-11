#include <Arduino.h>

#define RED_PIN 11    // Pin for red channel of RGB LED
#define GREEN_PIN 10  // Pin for green channel of RGB LED
#define BLUE_PIN 9    // Pin for blue channel of RGB LED

// Define brightness levels for each color channel (0-255)
int red_brightness = 0;
int green_brightness = 0;
int blue_brightness = 0;

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
  Serial.println("RGB LED initialized with brightness 0.");
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
      // Update LED with new brightness values
      analogWrite(RED_PIN, red_brightness);
      analogWrite(GREEN_PIN, green_brightness);
      analogWrite(BLUE_PIN, blue_brightness);
      // Print confirmation to serial monitor
      Serial.print("Set RGB to: ");
      Serial.print(red_brightness); Serial.print(", ");
      Serial.print(green_brightness); Serial.print(", ");
      Serial.println(blue_brightness);
    } else {
      // Print error if input format is invalid
      Serial.println("Invalid input. Use format: R,G,B");
    }
  }

  // Add a small delay to avoid overwhelming the serial buffer
  delay(100);
}
