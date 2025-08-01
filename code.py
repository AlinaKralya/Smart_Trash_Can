# ------------------- LIBRARIES ----------------------
import time
import board
import digitalio
import pwmio                                    # Used for Motors and Servo
import pulseio                                  # Used for Ultrasonic Sensor
import analogio                                 # Used for Microphone
from adafruit_motor import servo

# --------------------- SETUP ------------------------
# Motor A (Left)
in1 = digitalio.DigitalInOut(board.D5)          # IN1 & IN2 control direction
in1.direction = digitalio.Direction.OUTPUT
in2 = digitalio.DigitalInOut(board.D6)
in2.direction = digitalio.Direction.OUTPUT
ena = pwmio.PWMOut(board.D10, frequency=1000)   # ENA = pin to control the speed

# Motor B (Right)
in3 = digitalio.DigitalInOut(board.D3)          # IN3 & IN4 control direction
in3.direction = digitalio.Direction.OUTPUT
in4 = digitalio.DigitalInOut(board.D4)
in4.direction = digitalio.Direction.OUTPUT
enb = pwmio.PWMOut(board.D8, frequency=1000)    # ENB = pin to control the speed

# Servo
pwm = pwmio.PWMOut(board.D11, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

# Microphone
mic = analogio.AnalogIn(board.A1)
THRESHOLD = 6000                                # Adjust if need to pick up noise of the lower frequency

# Buzzer
buzzer = digitalio.DigitalInOut(board.D2)
buzzer.direction = digitalio.Direction.OUTPUT

# Ultrasonic Sensor
trig = digitalio.DigitalInOut(board.D12)        # Connecting Trigger
trig.direction = digitalio.Direction.OUTPUT
echo = pulseio.PulseIn(board.D13)               # Connecting Echo
echo.pause()
echo.clear()

# ------------------- FUNCTIONS ----------------------
# Measuring how full the trash can is
def get_distance():
    trig.value = True
    time.sleep(0.00001)
    trig.value = False

    echo.clear()
    echo.resume()

    timeout = time.monotonic() + 0.1
    while len(echo) == 0 and time.monotonic() < timeout:
        pass

    echo.pause()

    if len(echo) == 0:
        return None

    pulse_duration = echo[0] / 1_000_000        # Microseconds to seconds
    distance_cm = (pulse_duration * 34300) / 2
    return distance_cm

# Reading data from the microphone
def read_mic():
    return mic.value

#Count claps within timeout window
def count_claps(timeout=1.0):
    start = time.monotonic()
    clap_count = 1                              # First clap already detected
    while time.monotonic() - start < timeout:
        if read_mic() > THRESHOLD:
            clap_count += 1
            print(f"Clap {clap_count}")
            time.sleep(0.25)                    # Debounce
    return clap_count

# ------------------- MAIN LOOP ----------------------
while True:
    if read_mic() > THRESHOLD:
        print("Clap 1 detected")
        time.sleep(0.2)                         # Debounce
        num_claps = count_claps()

        if num_claps == 1:
            print("Single Clap → Motors")
            print("Forward for 5 seconds")

            # Set direction
            in1.value = True
            in2.value = False
            in3.value = True
            in4.value = False

            # Set speed (50%)
            ena.duty_cycle = int(0.5 * 65535)
            enb.duty_cycle = int(0.5 * 65535)

            # Wait for 5 seconds
            time.sleep(5)

            # Stop motors
            ena.duty_cycle = 0
            enb.duty_cycle = 0
            in1.value = False
            in2.value = False
            in3.value = False
            in4.value = False

            print("Stopped")

        # Opening the lid
        elif num_claps == 2:
            print("Double Clap → Open Lid")
            my_servo.angle = 180
            time.sleep(0.5)
            my_servo.angle = 0

        # Check the distance
        elif num_claps == 3:
            print("Triple Clap → Check Distance")
            dist = get_distance()
            if dist:
                print(f"Distance: {dist:.2f} cm")
                buzzer.value = dist < 20
                time.sleep(1)
                buzzer.value = False
            else:
                print("No distance measured")
                buzzer.value = False
        else:
            print(f"{num_claps} claps detected — no action assigned")

        time.sleep(1)                               # Cooldown to avoid repeat triggers
