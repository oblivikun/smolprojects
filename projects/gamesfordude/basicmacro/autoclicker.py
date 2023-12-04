from pynput.mouse import Listener as MouseListener, Button
from pynput.keyboard import Listener as KeyboardListener, Key, HotKey, KeyCode
import pyautogui
import time
import threading
import tkinter as tk


class MacroRecorder:
    def stop_macro(self):
        print("Stopping macro")
        self.playing = False
    def __init__(self):
        print("Initializing MacroRecorder")
        self.loop = False
        self.actions = []
        self.recording = False
        self.playing = False
        self.last_x = None
        self.last_y = None
        self.last_event_time = None

        self.stop_recording_hotkey = HotKey(
            {Key.shift, KeyCode.from_char('r')}, 
            self.stop_recording
        )
        self.stop_macro_hotkey = HotKey(
            {Key.shift, KeyCode.from_char('m')}, 
            self.stop_macro
        )

    def toggle_loop(self):
        print("Toggling loop")
        self.loop = not self.loop    

    def start_recording(self):
        print("Starting recording")
        self.recording = True
        self.mouse_listener = MouseListener(on_move=self.record_mouse, on_click=self.record_mouse)
        self.keyboard_listener = KeyboardListener(on_press=self.record_key_press, on_release=self.record_key_release)
        self.mouse_listener.start ()
        self.keyboard_listener.start()

    def stop_recording(self):
        print("Stopping recording")
        self.recording = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def record_mouse(self, x, y, button=None, pressed=None):
        print(f"Recording mouse event at ({x}, {y}) with button {button} and pressed {pressed}")
        current_time = time.time()
            
        if not self.recording:
            self.last_event_time = current_time
            return
            
        time_since_last_event = 0 if self.last_event_time is None else current_time - self.last_event_time
        self.last_event_time = current_time        
            
        if button is None and pressed is None:   
            event = 'move'
        else:
            event = 'press' if pressed else 'release'
        
        self.actions.append(('mouse', x, y, button, event, time_since_last_event))
        
    def record_key_press(self, key):
        print(f"Recording key press: {key}")
        current_time = time.time()
            
        if not self.recording:
            self.last_event_time = current_time
            return
            
        time_since_last_event = 0 if self.last_event_time is None else current_time - self.last_event_time
        self.last_event_time = current_time        

        self.actions.append(('key_press', key, time_since_last_event))

        self.stop_recording_hotkey.press(key)
        self.stop_macro_hotkey.press(key)

    def record_key_release(self, key):
        print(f"Recording key release: {key}")
        current_time = time.time()
            
        if not self.recording:
            self.last_event_time = current_time
            return
            
        time_since_last_event = 0 if self.last_event_time is None else current_time - self.last_event_time
        self.last_event_time = current_time        

        self.actions.append(('key_release', key, time_since_last_event))

        self.stop_recording_hotkey.release(key)
        self.stop_macro_hotkey.release(key)

    def play_macro(self):
        print("Playing macro")
        if self.playing: # If a macro is already playing, don't start another one
            return
        self.playing = True
        
        # Start the play_macro_thread in a new thread
        threading.Thread(target=self.play_macro_thread).start()

        # Start the stop_hotkey_listener thread
        threading.Thread(target=self.stop_hotkey_listener).start()

    def play_macro_thread(self):
        while self.playing and (self.loop or len(self.actions) > 0):
            action = self.actions.pop(0)
            print(f"Executing action: {action}")

            if len(self.actions) != 0:
                time_to_next_action = self.actions[0][-1] - action[-1]
                if time_to_next_action < 0:  
                    time_to_next_action = 0
                time.sleep(time_to_next_action)

            # Check action type and execute corresponding PyAutoGUI function
            if action[0] == 'mouse':
                if action[4] == 'move':
                    pyautogui.moveTo(action[1], action[2])  
                elif action[4] == 'press':
                    button = self.get_button_name(action[3])
                    pyautogui.mouseDown(action[1], action[2], button)
                elif action[4] == 'release':
                    button = self.get_button_name(action[3])
                    pyautogui.mouseUp(action[1], action[2], button)
            elif action[0] == 'key_press':
                pyautogui.keyDown(str(action[1]))   
            elif action[0] == 'key_release':
                pyautogui.keyUp(str(action[1]))
                
        if toggle_loop_button == False:
            self.playing = False
        

    def stop_hotkey_listener(self):
        listener = KeyboardListener(on_press=self.stop_hotkey_on_press)
        listener.start()


    def stop_hotkey_on_press(self, key):
        self.stop_recording_hotkey.press(key)
        self.stop_macro_hotkey.press(key)
        self.playing = False

    def stop_hotkey_listener(self):
        listener = KeyboardListener(on_press=self.stop_hotkey_on_press)
        listener.start()

    def stop_hotkey_on_press(self, key):
        self.stop_recording_hotkey.press(key)
        self.stop_macro_hotkey.press(key)   
        self.playing = False
            


    @staticmethod
    def get_button_name(button):
        print(f"Getting button name for {button}")
        if button == Button.left:
            return 'left'
        elif button == Button.right:
            return 'right'
        return 'middle'

macro_recorder = MacroRecorder()

def start_recording():
    print("Starting recording from main")
    macro_recorder.start_recording()

def stop_recording():
    print("Stopping recording from main")
    macro_recorder.stop_recording()

def play_macro():
    print("Playing macro from main")
    play_thread = threading.Thread(target=macro_recorder.play_macro)
    play_thread.start()

def stop_macro():
    print("Stopping macro from main")
    macro_recorder.stop_macro()

window = tk.Tk()
start_button = tk.Button(window, text="Start Recording", command=start_recording)
start_button.pack()
stop_button = tk.Button(window, text="Stop Recording", command=stop_recording)
stop_button.pack()
play_button = tk.Button(window, text="Play Macro", command=play_macro)
play_button.pack()
stop_play_button = tk.Button(window, text="Stop Macro", command=stop_macro)
stop_play_button.pack()
toggle_loop_button = tk.Button(window, text="Toggle Loop", command=macro_recorder.toggle_loop)
toggle_loop_button.pack()
window.mainloop()