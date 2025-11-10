#!/bin/env python3
import RPi.GPIO as GPIO
import time

# Set the GPIO pin number where the DHT sensor's data pin is connected.
LINEFAIL_PIN = 26

def linefail_callback():
    print("⚠️ Line fail detected! (pin shorted to ground)")
    time.sleep(60) # 60 seconds

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LINEFAIL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print(f"Reading pullup on GPIO {LINEFAIL_PIN}...")
    print("Press Ctrl+C to exit.")

    GPIO.add_event_detect(
        LINEFAIL_PIN, GPIO.FALLING, callback=linefail_callback, bouncetime=200
    )

    print("Monitoring UPS line fail on pin 37 (GPIO26). Press Ctrl+C to exit.")

has_linefailed = True 
while True:
    if has_linefailed:
        setup()

    if GPIO.event_detected(LINEFAIL_PIN):
        has_linefailed = True

    try:
        time.sleep(1)  # keep the script alive
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(0) 
    finally:
        if has_linefailed:
            try:
                GPIO.remove_event_detect(LINEFAIL_PIN)
            except: pass
            GPIO.cleanup()
            has_linefailed = False
