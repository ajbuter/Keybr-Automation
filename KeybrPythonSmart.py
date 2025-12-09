import pytesseract
from PIL import Image
import pyautogui
from pynput.keyboard import Controller, Key, Listener
import threading
import time
import random

keyboard = Controller()
start_typing = False
delay = 0.15 # default typing speed
delay = random.uniform(0.1, 0.16)

typing_script = []

# ---- Screenshot OCR function ----
def get_keybr_text():
    # Coordinates of the Keybr text area (adjust these manually)
    x, y, width, height = 350, 385, 850, 400 
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    text = pytesseract.image_to_string(screenshot)

    # # log screenshots
    # timestamp = int(time.time() * 1000)
    # filename = f"screenshot_{timestamp}.png"
    # screenshot.save(filename)
    # print(f"Saved screenshot as {filename}")
    
    # Clean up the text
    text = text.replace('\n', ' ').strip()
    return text

# ---- Typing function ----
def type_script():
    global start_typing
    for char, delay_time in typing_script:
        if not start_typing:
            break
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(delay_time)
    start_typing = False

# ---- Hotkey listener ----
def on_press(key):
    global start_typing, typing_script
    if key == Key.f8 and not start_typing:
        working = True
        print("Working Started")
        while working:
            print("F8 pressed: grabbing text and starting typing...")
            text_to_type = get_keybr_text()
            print("Text grabbed:", repr(text_to_type))
            delay = random.uniform(0.1,0.16)
            typing_script = [(c, delay) for c in text_to_type]
            start_typing = True
            threading.Thread(target=type_script).start()
            print("started sleep")
            time.sleep(17)
            print("5 seconds left")
            time.sleep(5)
    elif key == Key.esc:
        start_typing = False
        print("ESC pressed: stopped typing.")

    # # print cursor location with down arrow
    # elif key == key.down:
    #     print(pyautogui.position())

# ---- Main listener ----
with Listener(on_press=on_press) as listener:
    print("Press F8 to start typing (OCR grabs text), ESC to stop.")
    listener.join()
