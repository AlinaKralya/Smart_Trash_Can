# -------------- LIBRARIES -----------------
import time
import board
import pwmio
import usb_cdc
from adafruit_motor import servo

# ----------------- SETUP ------------------
pwm = pwmio.PWMOut(board.D5, duty_cycle=0, frequency=50)
lid_servo = servo.Servo(pwm)
lid_servo.angle = 0

# --------------- FUNCTIONS ----------------
def open_lid():
    print("Opening trash can")
    lid_servo.angle = 90 #Check if the angle is appropriate to open and close
    time.sleep(2)

def close_lid():
    print("Closing trash can")
    lid_servo.angle = 0
    time.sleep(2)

# -------------- MAIN LOOP -----------------
while True:
    if usb_cdc.data.im_waiting > 0:
        command = usb_cdc.data.readline().decode('utf-8').strip().lower()
        print(f"Received: {command}")

        if command == "open":
            open_lid()
        elif command == "close":
            close_lid()