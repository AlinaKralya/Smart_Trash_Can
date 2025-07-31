# ------------------- LIBRARIES ----------------------
import time
import board
import digitalio
import pwmio                                    # Used for Motors and Servo
import pulseio                                  # Used for Ultrasonic Sensor
import analogio                                 # Used for Microphone
from adafruit_motor import servo

# --------------------- SETUP ------------------------
# Buzzer
buzzer = digitalio.DigitalInOut(board.D2)
buzzer.direction = digitalio.Direction.OUTPUT

# Motor B (Right)
in3 = digitalio.DigitalInOut(board.D3)          # IN3 & IN4 control direction
in3.direction = digitalio.Direction.OUTPUT
in4 = digitalio.DigitalInOut(board.D4)
in4.direction = digitalio.Direction.OUTPUT
enb = pwmio.PWMOut(board.D8, frequency=1000)    # ENB = speed for motor B

# Motor A (Left)
in1 = digitalio.DigitalInOut(board.D5)          # IN1 & IN2 control direction
in1.direction = digitalio.Direction.OUTPUT
in2 = digitalio.DigitalInOut(board.D6)
in2.direction = digitalio.Direction.OUTPUT
ena = pwmio.PWMOut(board.D10, frequency=1000)   # ENA = speed for motor A

# Servo
pwm = pwmio.PWMOut(board.D11, duty_cycle=2 ** 15, frequency=50)
lid_servo = servo.Servo(pwm)

# Ultrasonic Sensor
trig = digitalio.DigitalInOut(board.D12)        # Connecting Trigger
trig.direction = digitalio.Direction.OUTPUT
echo = pulseio.PulseIn(board.D13)               # Connecting Echo
echo.pause()
echo.clear()

# Microphone
mic = analogio.AnalogIn(board.A1) 
THRESHOLD = 6000

# Threshold in cm (needs to be adjusted according to the can)
FULL_CAN = 10.0

# Constants for Servo
LID_OPEN_ANGLE = 90                             # Check if the angle is right to open and close
LID_CLOSED_ANGLE = 0

# ------------------- FUNCTIONS ----------------------
# Measuring how full the trash can is
def measure_distance_in_cm():

    # Initiating the measurements
    trig.value = False                          # Clearing previous signals, if any
    time.sleep(0.000002)                        # Letting the trigger to settle
    trig.value = True
    time.sleep(0.00001)                         # Sending a 10-microsecond HIGH pulse to start the measurement
    trig.value = False

    # Listening to the echo
    echo.clear()
    echo.resume()                               # Starts listening
    time.sleep(0.1)                             # Wait for the sensor to collect data
    echo.pause()

    # If there is no echo (measurement is not possible)
    if len(echo) == 0:
        return None

    # Calculate the distance
    pulse_duration = echo[0]
    distance_in_cm = pulse_duration / 5.83       # 5.83 is roughly a time for the roundtrip
    return distance_in_cm

# Opening the lid with Servo
def open_lid():
    print("Opening trash can")
    lid_servo.angle = LID_OPEN_ANGLE           
    time.sleep(2)

# Closing the lid with Servo
def close_lid():
    print("Closing trash can")
    lid_servo.angle = LID_CLOSED_ANGLE
    time.sleep(2)

# Reading data from the microphone
def read_mic():
    return mic.value

# Detecting clapping noise
def wait_for_clap(timeout=0.5):
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        if read_mic() > THRESHOLD:
            return True
    return False

# ------------------- MAIN LOOP ----------------------
while True:
    # Block of code for the measurement of how much trash is in the can
    distance = measure_distance_in_cm()

    # Checking distance output by the sensor
    if distance:
        # If the trash can is full
        if distance <= FULL_CAN:
            # Keep buzzing until trash can is not full anymore
            while distance <= FULL_CAN:
                buzzer.value = True
                time.sleep(0.5)
                buzzer.value = False
                time.sleep(0.5)

                # Update distance while buzzing
                distance = measure_distance_in_cm()
        # Turn off the buzzer
        else:
            buzzer.value = False
    else:
        print("No echo received")
    time.sleep(1)

    # Block of code to move the trash can and open the lid by clapping
    if read_mic() > THRESHOLD:
        print("Clap 1 detected")
        time.sleep(0.2)  # Debounce delay

        if wait_for_clap(0.4):  # Wait 400ms 
            print("Double Clap Detected -> Open Lid")
            open_lid()    # Opening
            time.sleep(5)
            close_lid()    # Closing
        else:
            print("Single Clap Detected -> Move Forward")
            # Motor A moving forward at 50%
            in1.value = True
            in2.value = False
            ena.duty_cycle = int(0.5 * 65535)

            # Motor B moving at 50% as well
            in3.value = True
            in4.value = False
            enb.duty_cycle = int(0.5 * 65535)

            time.sleep(5)
        time.sleep(2)  # Cooldown to avoid rapid triggers
