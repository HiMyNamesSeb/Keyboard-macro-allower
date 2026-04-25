#----------------------------------------------------- imports
import record
import playback
import threading

#----------------------------------------------------- setup pynput and listeners
from pynput import keyboard, mouse
m_listener = mouse.Listener(on_click=record.on_mouse_click , on_move=record.on_mouse_move)
k_listener = keyboard.Listener(on_press=record.on_key_press)
m_listener.start()
k_listener.start()

#----------------------------------------------------- setup customtkinter app window
import customtkinter
app = customtkinter.CTk()

#----------------------------------------------------- variables
#customize button keybinds in record.py
isLooping = False
OUTPUT_FILE = "recording.json"
#----------------------------------------------------- Start Recording button
def startRecordingEvent(): #
    record.flipIsRecording()
    record.clear_recordings()
    print("you are now recording")
startRecording = customtkinter.CTkButton(master= app, command = startRecordingEvent , text = "start recording" )
startRecording.pack()

#----------------------------------------------------- End Recording button

def endRecordingEvent():
    record.flipIsRecording()
    record.save_recording()
    print("you stopped recording")
endRecording = customtkinter.CTkButton(master= app, command = endRecordingEvent , text = "stop recording" )
endRecording.pack()

#----------------------------------------------------- Single Playback button
def singlePlaybackEvent():
    playback.playback(playback.load_recording())
singlePlayback = customtkinter.CTkButton(master= app, command = singlePlaybackEvent , text = "playback" )
singlePlayback.pack()

#----------------------------------------------------- Loop Playback button
def loopPlaybackEvent():
    global isLooping
    isLooping = True
    t = threading.Thread(target=loop_playback)
    t.daemon = True  # thread dies when the app closes
    t.start()
loopPlayback = customtkinter.CTkButton(master= app, command = loopPlaybackEvent , text = "start loop" )
loopPlayback.pack()

#----------------------------------------------------- playback loop logic functions
def loop_playback():
    record.stop_event.clear()  # reset it before starting
    print("starting loop")
    while not record.stop_event.is_set():
        playback.playback(playback.load_recording())

#----------------------------------------------------- Small customtikinter details
customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")
app.geometry("200x120")
app.attributes("-topmost", True)
app.title("Macro Overlay")
app.resizable(width=False, height=False)
app.mainloop() #launch the window
