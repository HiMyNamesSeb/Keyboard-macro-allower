#----------------------------------------------------- imports
import json
import time
from pynput import keyboard, mouse
import threading
#----------------------------------------------------- variables
stop_event = threading.Event()

OUTPUT_FILE = "recording.json"

flipKey = "["
stopKey = "]"
isRecording = False
events = []
#----------------------------------------------------- simple helper functions
def flipIsRecording(): # flips the isRecording bool
    global isRecording
    if isRecording:
        isRecording = False
    else:
        isRecording = True

def clear_recordings(): # wipes the .json file clean
    global events
    events = []
    open(OUTPUT_FILE, "w").close()

def save_recording(): # writes to the .json file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(events, f, indent=2)
#----------------------------------------------------- KEYBOARD , on press
def on_key_press(key):
    global isRecording

    keyData = str(key)
    keyData = keyData.replace("'", "") # remove ugly ''

    if keyData == stopKey: #set the stopper to true and stop playing
        stop_event.set()
        return
    if keyData == flipKey:
        if isRecording: # if you're recording and click this stop recording
            print("\n you have stopped recording")
            isRecording = False
            save_recording()
        return
    if not isRecording:  # lets you type without recording by accident
        return
#-------------------------- Event dictionary being created
    events.append({
        "type": "key",
        "key": keyData,
        "time": time.time()
    })
#----------------------------------------------------- MOUSE , on click
def on_mouse_click(x, y, button, pressed):
    global isRecording
    if not isRecording: # check if its recording
        return
# -------------------------- Event dictionary being created
    events.append({
        "type": "mouse",
        "state": "press",
        "x": x, # the x and y are probably redundant, but it's fine
        "y": y,
        "button": str(button),
        "pressed": pressed,
        "time": time.time()
    })
    # ----------------------------------------------------- MOUSE , on move
def on_mouse_move(x, y, button):

    global isRecording
    if not isRecording: # check if its recording
        return
# -------------------------- Event dictionary being created
    events.append({
        "type": "mouse",
        "state": "move",
        "x": x,
        "y": y,
        "button": str(button),
        "time": time.time()
    })
