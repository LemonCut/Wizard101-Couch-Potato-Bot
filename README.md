# Wizard101 Couch Potato Bot

An automated farming bot for Wizard101 to farm Troubled Warriors for Couch Potato seeds.

## Features

- Automatically searches for and engages the "Troubled Warrior" enemy
- Combat automation with card selection and pass functionality (targets Ship of Fools)
- Mana monitoring and automatic potion usage
- Screen capture and OCR text recognition for game state detection
- Randomized movements to mimic human behavior

## Technologies Used

### Core Technologies

- **Python** - Main programming language
- **OpenCV (cv2)** - Computer vision and image processing
- **PyAutoGUI** - Mouse and keyboard automation
- **Pytesseract** - OCR (Optical Character Recognition) for reading in-game text
- **NumPy** - Array operations and image processing support

### How It Works

The bot uses:

- **Template matching** to identify game UI elements (cards, buttons, icons)
- **OCR text recognition** to detect quest text and combat state
- **Color filtering** to isolate yellow game text from screenshots
- **Automated mouse/keyboard control** to navigate and perform actions

### Utility Scripts

- `get_mouse_position.py` - Helper to find coordinates for clicking positions
- `test_mouse_down.py` - Test script for mouse drag functionality

## Disclaimer

This bot is for educational purposes only. Use of automation tools may violate the game's terms of service.
