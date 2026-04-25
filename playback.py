#----------------------------------------------------- imports
import json
from time import sleep
from pynput import mouse, keyboard
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
import record
#----------------------------------------------------- variables
button_map = {
    "Button.left": mouse.Button.left,
    "Button.right": mouse.Button.right,
    "Button.middle": mouse.Button.middle
}
kb = KeyboardController()
mc = MouseController()
OUTPUT_FILE = "recording.json"
#----------------------------------------------------- loads all the events in the .json file
def load_recording():
    with open(OUTPUT_FILE, "r") as f:
        return json.load(f)
#----------------------------------------------------- reads a file plays all the inputs in the .json
def playback(events):
    for i, event in enumerate(events):

        if record.stop_event.is_set(): # ends early if you initiate the end
            return

        if i==0:
            delay = 0 #the first item has no reference so 0 delay
        else:
            delay = events[i]["time"] - events[i - 1]["time"] #time math

        sleep(delay) #delay

        if event["type"] == "key": # for keyboard
            if event["type"] == "key":
                if event["key"].startswith("Key."): # for special keys like tab, enter, space etc
                    special_key = getattr(keyboard.Key, event["key"].replace("Key.", ""))
                    kb.press(special_key)
                    kb.release(special_key)
                else: #for other keys
                    kb.press(keyboard.KeyCode.from_char(event["key"])) #converts into an object that .press can pass
                    kb.release(keyboard.KeyCode.from_char(event["key"]))

        elif event["type"] == "mouse": # for mouse
            if event["state"] == "press":                           # on click
                if event["pressed"]:
                    mc.position = (event["x"], event["y"]) # REDUNDANT, could be moved, but it's good just incase
                    mc.click(button_map[event["button"]], 1)
            if event["state"] == "move":                            # on move
                mc.position = (event["x"], event["y"])
