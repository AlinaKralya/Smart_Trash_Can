# --------------- LIBRARIES ----------------
import time
import board
import digitalio
import pulseio # Needed to measure how long the Echo pin stays HIGH

# ----------------- SETUP ------------------

# Trigger pin
trigger = digitalio.DigitalInOut(board.D3)
trigger.direction = digitalio.Direction.OUTPUT

# Echo pin
echo = pulseio.PulseIn(board.D2)
echo.pause()
echo.clear()

# Buzzer
buzzer = digitalio.DigitalInOut(board.D4)
buzzer.direction = digitalio.Direction.OUTPUT

# Threshold in cm (needs to be adjusted according to the can)
FULL_CAN = 10.0

# --------------- FUNCTIONS ----------------
def measure_distance_in_cm():

    # Initiating the measurements
    trigger.value = False       # Clearing previous signals, if any
    time.sleep(0.000002)        # Letting the trigger to settle
    trigger.value = True
    time.sleep(0.00001)         # Sending a 10-microsecond HIGH pulse to start the measurement
    trigger.value = False

    # Listening to the echo
    echo.clear()
    echo.resume()               # Starts listening
    time.sleep(0.1)             # Wait for the sensor to collect data
    echo.pause()

    # If there is no echo (measurement is not possible)
    if len(echo) == 0:
        return None

    # Calculate the distance
    pulse_duration = echo[0]
    distance_in_cm = pulse_duration / 5.83       # 5.83 is roughly a time for the roundtrip (math in the google doc)

# ---------------- MAIN LOOP ---------------
while True:
    distance = measure_distance_cm()

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
                distance = measure_distance_cm()

        # Turn off the buzzer
        else:
            buzzer.value = False

    else:
        print("No echo received")
    time.sleep(1)