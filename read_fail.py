#!/bin/env python3
import RPi.GPIO as rGPIO
import time

# Set the rGPIO pin number where the DHT sensor's data pin is connected.
LINEFAIL_PIN = 26

def linefail_callback():
    print("⚠️ Line fail detected! (pin shorted to ground)")
    time.sleep(60) # 60 seconds

def setup():
    rGPIO.setmode(rGPIO.BCM)
    rGPIO.setup(LINEFAIL_PIN, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)

    print(f"Reading pullup on rGPIO {LINEFAIL_PIN}...")
    print("Press Ctrl+C to exit.")

    rGPIO.add_event_detect(
        LINEFAIL_PIN, rGPIO.FALLING, callback=linefail_callback, bouncetime=200
    )

    print("Monitoring UPS line fail on pin 37 (rGPIO26). Press Ctrl+C to exit.")

has_linefailed = True 
while True:
    if has_linefailed:
        setup()

    if rGPIO.event_detected(LINEFAIL_PIN):
        has_linefailed = True

    try:
        time.sleep(1)  # keep the script alive
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(0) 
    finally:
        if has_linefailed:
            try:
                rGPIO.remove_event_detect(LINEFAIL_PIN)
            except: pass
            rGPIO.cleanup()
            has_linefailed = False
