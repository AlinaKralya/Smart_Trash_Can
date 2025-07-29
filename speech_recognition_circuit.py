# --------------- LIBRARIES ----------------
import board
import digitalio
import supervisor
import time

# Set up an LED to trigger
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# --------------- MAIN LOOP ----------------
while True:
    if supervisor.runtime.serial_bytes_available:
        command = input().strip()
        print("Received:", command)

        if command == "OPEN":
            led.value = True
            time.sleep(2)
            led.value = "False"