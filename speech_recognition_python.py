# ---------------- LIBRARIES ---------------
import speech_recognition as sr
import serial
import time

'''
To make speech_recognition and serial work, follow those steps:
1. Go to the terminal or PowerShell on your operational system
2. Install speech_recognition library ( pip install SpeechRecognition )
2. Install pyaudio ( pip install PyAudio )
3. Install serial ( python -m pip install pyserial )
4. Restart the VS Code
5. Go to Debugging menu and run it, so the system detects new libraries
'''
# ---------------- SETUP -------------------
# Serial connection with CircuitPython board
ser = serial.Serial('COM6', 9600, timeout=1) # Change 'COM6' depending on your laptop
time.sleep(2) # Allow connection to establish

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("Say 'Open' to activate...")

# -------------- MAIN LOOP -----------------
while True:
    with mic as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("Heard: ", command)

        if "open" in command:
            print("\nCommand recognized. Sending to the board...")
            ser.write(b"OPEN\n") # Send signal
        else:
            print("\nCommand not recognized.")

    except sr.UnknownValueError:
        print("\nCouldn't understand the audio")
    except sr.RequestError as e:
        print(f"API error: {e}")