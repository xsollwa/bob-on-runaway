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

# Stepper Motors with TMC2209 (STEP, DIR, EN)
motorA = {'STEP': 15, 'DIR': 14, 'EN': 18}  # Left motor
motorB = {'STEP': 6,  'DIR': 26, 'EN': 5}   # Right motor

for motor in [motorA, motorB]:
    GPIO.setup(motor['STEP'], GPIO.OUT)
    GPIO.setup(motor['DIR'], GPIO.OUT)
    GPIO.setup(motor['EN'], GPIO.OUT)
    GPIO.output(motor['EN'], GPIO.LOW)  # Enable motor

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

def move_motor(motor, steps, delay=0.001):
    """
    Move a stepper motor using TMC2209.

    Args:
        motor (dict): Dictionary with 'STEP', 'DIR', and 'EN' keys.
        steps (int): Number of steps to move. Positive = forward, Negative = reverse.
        delay (float): Delay between steps.
    """
    direction = GPIO.HIGH if steps > 0 else GPIO.LOW
    GPIO.output(motor['DIR'], direction)
    steps = abs(steps)

    for _ in range(steps):
        GPIO.output(motor['STEP'], GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(motor['STEP'], GPIO.LOW)
        time.sleep(delay)


def move_backward():
    move_motor(motorA, -512)
    move_motor(motorB, -512)

def turn_left():
    move_motor(motorA, -512)
    move_motor(motorB, 512)

def turn_right():
    move_motor(motorA, 512)
    move_motor(motorB, -512)

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
