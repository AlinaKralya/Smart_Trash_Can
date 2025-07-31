# type: ignore
import time
import board
import digitalio
import pwmio
import pulseio
import analogio
from adafruit_motor import servo

# === Servo Setup (for double clap) ===
# Motor A (Left)
in1 = digitalio.DigitalInOut(board.D5)
in1.direction = digitalio.Direction.OUTPUT

in2 = digitalio.DigitalInOut(board.D6)
in2.direction = digitalio.Direction.OUTPUT

ena = pwmio.PWMOut(board.D10, frequency=1000)  # ENA = speed for motor A D8

# Motor B (Right)
in3 = digitalio.DigitalInOut(board.D3)
in3.direction = digitalio.Direction.OUTPUT

in4 = digitalio.DigitalInOut(board.D4)
in4.direction = digitalio.Direction.OUTPUT

enb = pwmio.PWMOut(board.D8, frequency=1000)  # ENB = speed for motor B

pwm = pwmio.PWMOut(board.D11, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

# === Microphone Setup ===
mic = analogio.AnalogIn(board.A1)
THRESHOLD = 6000  # adjust if needed

def read_mic():
    return mic.value

def count_claps(timeout=1.0):
    """Count claps within timeout window."""
    start = time.monotonic()
    clap_count = 1  # first clap already detected
    while time.monotonic() - start < timeout:
        if read_mic() > THRESHOLD:
            clap_count += 1
            print(f"Clap {clap_count}")
            time.sleep(0.25)  # debounce
    return clap_count

# === Ultrasonic Distance Sensor Setup ===
trig = digitalio.DigitalInOut(board.D12)
trig.direction = digitalio.Direction.OUTPUT

echo = pulseio.PulseIn(board.D13)
echo.pause()
echo.clear()

# === Buzzer Setup ===
buzzer = digitalio.DigitalInOut(board.D2)
buzzer.direction = digitalio.Direction.OUTPUT

def get_distance():
    """Measure distance using ultrasonic sensor."""
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

    pulse_duration = echo[0] / 1_000_000  # microseconds to seconds
    distance_cm = (pulse_duration * 34300) / 2
    return distance_cm

# === MAIN LOOP ===
while True:
    if read_mic() > THRESHOLD:
        print("Clap 1 detected")
        time.sleep(0.2)  # debounce
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
        elif num_claps == 2:
            print("Double Clap → Open Lid")
            my_servo.angle = 180
            time.sleep(0.5)
            my_servo.angle = 0
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

        time.sleep(1)  # cooldown to avoid repeat triggers
