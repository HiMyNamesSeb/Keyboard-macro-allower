import json
import time
from time import sleep
from pynput import mouse

button_map = {
    "Button.left": mouse.Button.left,
    "Button.right": mouse.Button.right,
    "Button.middle": mouse.Button.middle
}
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController

kb = KeyboardController()
mc = MouseController()
OUTPUT_FILE = "recording.json"

def load_recording():
    with open(OUTPUT_FILE, "r") as f:
        return json.load(f)

def playback(events):
    # YOUR JOB: loop through events and replay each one
    for i, event in enumerate(events):
        # figure out the delay before this event
        # if it's not the first event, sleep for the difference
        # between this event's time and the previous event's time
        if i==0:
            delay = 0
        else:
            delay = events[i]["time"] - events[i - 1]["time"]
        sleep(delay)
        if event["type"] == "key":
            kb.type(event["key"])
            pass
        elif event["type"] == "mouse":
            if event["pressed"]:
                mc.position = (event["x"], event["y"])
                mc.click(button_map[event["button"]], 1)

            pass
playback(load_recording())