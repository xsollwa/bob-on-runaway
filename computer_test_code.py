# Imports 
import cv2
import time

# Setup 
servo_angle = 90
center_margin = 100  # pixels from center before robot turns

# Simulated Stepper Sequences
motorA_pins = [4, 18, 23, 24]  # Left motor
motorB_pins = [5, 6, 13, 19]   # Right motor 
seq = [[1,0,0,1],[1,0,0,0],[1,1,0,0],[0,1,0,0],
       [0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1]]

# Webcam 
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Functions 

def set_angle(angle):
    print(f"[SERVO] Rotating to angle: {angle}°")
    time.sleep(0.3)

def move_motor(label, steps, delay=0.002):
    direction = 1 if steps > 0 else -1
    steps = abs(steps)

    print(f"[{label}] Moving {steps} steps {'FORWARD' if direction == 1 else 'BACKWARD'}")
    for i in range(min(steps, 16)):  # Show only 16 steps to avoid spamming
        print(f"  [step {i+1}] {seq[i % 8]}")
        time.sleep(delay)

def move_backward():
    move_motor("MOTOR A", -512)
    move_motor("MOTOR B", -512)

def turn_left():
    move_motor("MOTOR A", -512)
    move_motor("MOTOR B", 512)

def turn_right():
    move_motor("MOTOR A", 512)
    move_motor("MOTOR B", -512)

# Main Loop 
set_angle(servo_angle)

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        h, w, _ = frame.shape
        frame_center = w // 2
        action_text = "[ACTION] Idle"

        # center line
        cv2.line(frame, (frame_center, 0), (frame_center, h), (255, 255, 255), 1)

        if len(faces) > 0:
            (x, y, fw, fh) = faces[0]
            face_center = x + fw // 2

            # Draw bounding box + info
            cv2.rectangle(frame, (x, y), (x + fw, y + fh), (0, 255, 0), 2)
            cv2.putText(frame, f"Face center: {face_center}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(frame, f"Frame center: {frame_center}", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            # Servo tracking
            if face_center < frame_center - 50 and servo_angle < 180:
                servo_angle += 5
                set_angle(servo_angle)
            elif face_center > frame_center + 50 and servo_angle > 0:
                servo_angle -= 5
                set_angle(servo_angle)

            # Robot movement 
            if face_center < frame_center - center_margin:
                action_text = "[ACTION] Turn RIGHT"
                turn_right()
            elif face_center > frame_center + center_margin:
                action_text = "[ACTION] Turn LEFT"
                turn_left()
            else:
                action_text = "[ACTION] Back up!"
                move_backward()

        else:
            cv2.putText(frame, "No face detected", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        #Action on screen
        cv2.putText(frame, action_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # Display video
        cv2.imshow('Robot Vision (Simulation)', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cam.release()
    print("[CLEANUP] Done")
    cv2.destroyAllWindows()
