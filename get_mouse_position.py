import pyautogui
import time

"""
    Helper program to get mouse location data from pyautogui.
"""

print("Move your mouse to the desired location and press 'Ctrl+C' to stop.")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})", end="\n")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nProgram terminated.")