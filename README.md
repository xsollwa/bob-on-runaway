# bob-on-runaway
**Bob runs from you -- Undercity**

A Raspberry Pi based robot that uses a webcam to detect human faces and run away from them while avoiding obstacles in real time.

**Created by:** Ryan Davis, Ruzanna Gaboyan and Philip Golczak  
**Date:** July 14, 2025  

## Features: What It Does

- Detects human faces using OpenCV
- Rotates the webcam toward the face using a servo motor
- Measures how close the person is using an ultrasonic sensor
- If the person is within 1 meter, Bob runs away and
- Avoids bumping into objects using 3 other ultrasonic sensors

## Pictures

**3d Model**

**Circuit board**

**Wiring Diagram**

<img width="775" height="615" alt="image" src="https://github.com/user-attachments/assets/d4084d28-a876-4136-95bd-388a01c552b0" />


**Final Assembly**

## Materials: How It Works

**Bill of Materials**
| Part         | Function                                      |
|------------------|-----------------------------------------------|
| Raspberry Pi 4    | Main controller (runs the code)              |
| USB Webcam        | Captures video for face detection            |
| Servo Motor       | Rotates the camera to follow the face        |
| Stepper Motors x2 | Drive the robot left, right, or backward     |
| Ultrasonic x4     | Detect people (front) + avoid obstacles (L/R/back) |
| Buck Converter |  |
| Switch |  | 
| Resistor 6x | |
| Perf board |  |
| Stepper Motor Drivers x2 |  |


## Setup Instructions

### 1. Raspberry Pi OS
- Flash Raspberry Pi OS to a microSD card 
- ....

### 2. Install Python Dependencies
...
