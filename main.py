import json
import time
from pynput import keyboard, mouse

TOGGLE_KEY = keyboard.Key.f8
OUTPUT_FILE = "recording.json"

flipKey = "["
isRecording = False
events = []

def on_key_press(key):
    global isRecording
    keyData = str(key)
    keyData = keyData.replace("'", "")
    if keyData == flipKey:
        if isRecording:
            print("\n you have stopped recording")
            isRecording = False
            save_recording()
        elif not isRecording:
            isRecording = True
            print("\n you are now recording")
            return
    if not isRecording:
        return
    if keyData == 'Key.space':
        keyData = ' '
    if keyData == 'Key.shift_r' or keyData == 'Key.shift':
        keyData = ''
    if keyData == 'Key.enter':
        keyData = '\n'

    events.append({
        "type": "key",
        "key": keyData,
        "time": time.time()
    })

def on_mouse_click(x, y, button, pressed):

    global isRecording
    if not isRecording:
        return
    events.append({
        "type": "mouse",
        "x": x,
        "y": y,
        "button": str(button),
        "pressed": pressed,
        "time": time.time()
    })

    pass

def save_recording():
    # YOUR JOB: write events list to OUTPUT_FILE as JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(events, f, indent=2)
    pass

# Start both listeners
with mouse.Listener(on_click=on_mouse_click) as m_listener, \
     keyboard.Listener(on_press=on_key_press) as k_listener:
    k_listener.join()


