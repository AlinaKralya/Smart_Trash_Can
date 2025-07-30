# type: ignore
import time
import board
import digitalio
import pwmio
import pulseio
import analogio


from adafruit_motor import servo

#Servo test code

# Create a PWMOut object on Pin D11
pwm = pwmio.PWMOut(board.D11, duty_cycle=2 ** 15, frequency=50)

# Create a servo object from the PWM 
my_servo = servo.Servo(pwm)
"""
while True:
    print("Turning to 0°")
    my_servo.angle = 0
    time.sleep(1)

    print("Turning to 90°")
    my_servo.angle = 90
    time.sleep(1)

    print("Turning to 180°")
    my_servo.angle = 180
    time.sleep(1)
"""

#mic that hears a clap vs 2 claps
#need to link motors going forward like for 5 secs for one clap and double clap makes the servo open
"""
mic = analogio.AnalogIn(board.A1) 
THRESHOLD = 6000 

def read_mic():
    return mic.value

def wait_for_clap(timeout=0.5):
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        if read_mic() > THRESHOLD:
            return True
    return False

while True:
    if read_mic() > THRESHOLD:
        print("Clap 1 detected")
        time.sleep(0.2)  # Debounce delay

        if wait_for_clap(0.4):  # Wait 400ms 
            print("Double Clap Detected -> Open Lid")
            
        else:
            print("Single Clap Detected -> Move Forward")
            

        time.sleep(1)  # Cooldown to avoid rapid triggers
"""

#The sensor and buzzer are linked, no need to touch it, just have to measure diameter of can

"""
# Setup for ultrasonic sensor
trig = digitalio.DigitalInOut(board.D12)
trig.direction = digitalio.Direction.OUTPUT

echo = pulseio.PulseIn(board.D13)
echo.pause()
echo.clear()

# Setup for buzzer
buzzer = digitalio.DigitalInOut(board.D2)
buzzer.direction = digitalio.Direction.OUTPUT

def get_distance():
    # Send a 10us pulse to trigger
    trig.value = True
    time.sleep(0.00001)
    trig.value = False

    echo.clear()
    echo.resume()

    # Wait for a valid pulse
    timeout = time.monotonic() + 0.1
    while len(echo) == 0 and time.monotonic() < timeout:
        pass

    echo.pause()

    if len(echo) == 0:
        return None  # No pulse received

    pulse_duration = echo[0] / 1_000_000  # Convert to seconds
    distance_cm = (pulse_duration * 34300) / 2  # Speed of sound = 34300 cm/s
    return distance_cm

while True:
    dist = get_distance()
    if dist:
        print(f"Distance: {dist:.2f} cm")
        if dist < 10:  # threshold in cm
            buzzer.value = True
        else:
            buzzer.value = False
    else:
        print("No distance measured")
        buzzer.value = False

    time.sleep(0.1)
"""

#Motor stuff, need to link this to the one clap of the mic + only make it run for like 5 sec 

"""
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

#
#while True:
    print("Forward")
    in1.value = True
    in2.value = False
    ena.duty_cycle = int(0.5 * 65535)  # Motor A at 50%

    in3.value = True
    in4.value = False
    enb.duty_cycle = int(0.5 * 65535)  # Motor B at 50%

    time.sleep(2)
"""
