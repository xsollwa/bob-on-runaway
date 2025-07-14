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

<img width="1642" height="924" alt="sure_2025-Jul-14_11-35-04AM-000_CustomizedView6653682117" src="https://github.com/user-attachments/assets/f31d8cbb-0e49-4b59-b2e6-bbff4c00d774" />


<img width="1337" height="844" alt="Screenshot 2025-07-14 042921" src="https://github.com/user-attachments/assets/fd023417-e59b-4eee-87d2-34c96da43155" />


**Circuit board**

![IMG_4653](https://github.com/user-attachments/assets/be024c4c-0b9c-4edd-acd4-c9e673d0e6b5)


**Wiring Diagram**

<img width="775" height="615" alt="image" src="https://github.com/user-attachments/assets/d4084d28-a876-4136-95bd-388a01c552b0" />


**Final Assembly**

![IMG_4654](https://github.com/user-attachments/assets/22272c27-84d3-4fb7-a654-03299a8065f6)

![IMG_4655](https://github.com/user-attachments/assets/c4379ad5-d913-4bf0-83ba-331bf641799c)


## Materials: How It Works

**Bill of Materials**
| Component                         | Description                                              |
|----------------------------------|----------------------------------------------------------|
| **Raspberry Pi 4**               | Main controller (runs the code)                          |
| **USB Webcam (Logitech C270)**   | Captures video for face detection using OpenCV          |
| **Servo Motor (9g)**             | Rotates the camera to follow the face                   |
| **Stepper Motors x2**            | Drive the robot left, right, or backward                |
| **Ultrasonic Sensors x3**        | Detect people and obstacles (front, left, right)        |
| **Buck Converter**               | Steps down battery voltage (7.4V to 5V for Pi)      |
| **Battery Pack (7.4V and 6V)**   | Powers motors and Pi (via buck converter)               |
| **Perf Board**                   | For mounting and soldering sensor/motor connections     |
| **Resistors x6**    | Protect GPIO       |



## Setup Instructions

### 1. Raspberry Pi OS
- Flash Raspberry Pi OS to a microSD card 
- SSH into Pi and configure network settings if necesary
- Install VNC via SSH
- Exit and VCN into pi
- Install ffmpeg for video viewing, use command ffview /dev/video0

### 2. Install Python Dependencies
sudo apt update
sudo apt upgrade -y
sudo apt install -y \
    python3-opencv \
    python3-pip \
    python3-numpy \
    python3-rpi.gpio \
    libatlas-base-dev \
    libhdf5-dev \
    libhdf5-103 \
    libjasper-dev \
    libqtgui4 \
    libqt4-test \
    wget \
    thonny

pip3 install numpy RPi.GPIO
wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml -O ~/haarcascade_frontalface_default.xml


