import pytesseract
from PIL import Image
import pyautogui
from pynput.keyboard import Controller, Key, Listener
import threading
import time
import random

keyboard = Controller()
typing = False
delay = 0.15 # default typing speed

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
    global typing, delay, typing_script
    for char, delay_time in typing_script:
        if not typing:
            break
        delay_time = random.uniform(0.1,0.16)
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(delay_time)

        # # print the active delay
        # print('Delay currently is:', delay)

    if typing:
        type_process()

def type_setup():
    global typing, typing_script
    print("F8 pressed: grabbing text and starting typing...")
    text_to_type = get_keybr_text()
    print("Text grabbed:", repr(text_to_type))
    typing_script = [(c, delay) for c in text_to_type]
    typing = True

def type_process():
    type_setup()
    threading.Thread(target=type_script).start()

# ---- Hotkey listener ----
def on_press(key):
    global typing
    # Begin Typing
    if key == Key.f8 and not typing:
        type_process()
    # Stop Typing
    elif key == Key.esc:
        typing = False
        print("ESC : stopped typing.", typing)
    # print cursor location with down arrow
    elif key == Key.down:
        print(pyautogui.position())

# ---- Main listener ----
with Listener(on_press=on_press) as listener:
    print("Press F8 to start typing, ESC to stop.")
    listener.join()
