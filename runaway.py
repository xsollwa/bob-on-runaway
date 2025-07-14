import cv2
import time
import RPi.GPIO as GPIO

# config
servo_angle = 90
center_margin = 100
face_size_threshold = 180  # Face width threshold for running

# GPIO Setup 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Servo Motor 
servo_pin = 13
GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50)
servo.start(0)

# Stepper Motors 
motorA_pins = [15, 14, 18, 13]  # L
motorB_pins = [6, 26, 5, 19]    # R

for pin in motorA_pins + motorB_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

step_seq = [
    [1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0],
    [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]
]

# Ultrasonic Sensors 
ultrasonic_pins = {
    'right': {'trig': 17, 'echo': 27},
    'front': {'trig': 25, 'echo': 22},
    'left': {'trig': 24, 'echo': 23}
}

for sensor in ultrasonic_pins.values():
    GPIO.setup(sensor['trig'], GPIO.OUT)
    GPIO.setup(sensor['echo'], GPIO.IN)

# Camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Functions
def set_angle(angle):
    duty = 2 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)
    servo.ChangeDutyCycle(0)

def move_motor(pins, steps, delay=0.002):
    direction = 1 if steps > 0 else -1
    steps = abs(steps)
    for _ in range(steps):
        for halfstep in range(8)[::direction]:
            for i in range(4):
                GPIO.output(pins[i], step_seq[halfstep][i])
            time.sleep(delay)

def move_backward():
    move_motor(motorA_pins, -512)
    move_motor(motorB_pins, -512)

def turn_left():
    move_motor(motorA_pins, -512)
    move_motor(motorB_pins, 512)

def turn_right():
    move_motor(motorA_pins, 512)
    move_motor(motorB_pins, -512)

def get_distance(trig, echo):
    GPIO.output(trig, False)
    time.sleep(0.01)
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    pulse_start = time.time()
    timeout = pulse_start + 0.05

    while GPIO.input(echo) == 0 and time.time() < timeout:
        pulse_start = time.time()

    while GPIO.input(echo) == 1 and time.time() < timeout:
        pulse_end = time.time()
    else:
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    return round(duration * 17150, 2)

# loop
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

        front_dist = get_distance(**ultrasonic_pins['front'])
        left_dist = get_distance(**ultrasonic_pins['left'])
        right_dist = get_distance(**ultrasonic_pins['right'])

        if len(faces) > 0:
            (x, y, fw, fh) = faces[0]
            face_center = x + fw // 2

            # Servo tracking
            if face_center < frame_center - 50 and servo_angle < 180:
                servo_angle += 5
                set_angle(servo_angle)
            elif face_center > frame_center + 50 and servo_angle > 0:
                servo_angle -= 5
                set_angle(servo_angle)

            # face size
            if fw > face_size_threshold:
                if front_dist < 30:
                    action_text = "[AVOID] Front Obstacle"
                elif left_dist < 30:
                    action_text = "[AVOID] Left Obstacle"
                    turn_right()
                elif right_dist < 30:
                    action_text = "[AVOID] Right Obstacle"
                    turn_left()
                else:
                    action_text = "[ACTION] Backing up"
                    move_backward()

        print(action_text)
        cv2.putText(frame, action_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.imshow('Robot Vision', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cam.release()
    servo.stop()
    GPIO.cleanup()
    cv2.destroyAllWindows()
    print("[CLEANUP] Done")
