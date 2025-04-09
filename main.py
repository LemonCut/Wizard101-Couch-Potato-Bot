import cv2
import numpy as np
import pyautogui
import pytesseract
import time
import random

# Set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Paths to the template images for playable (colored) and unplayable (grayscale) cards and the shop icon
PLAYABLE_CARD_TEMPLATE_PATH = 'images/playable_card.png'
UNPLAYABLE_CARD_TEMPLATE_PATH = 'images/unplayable_card.png'
SHOP_ICON_TEMPLATE_PATH = 'images/shop_icon.png'

# Coordinates of the "PASS" button (update with actual coordinates)
PASS_BUTTON_X, PASS_BUTTON_Y = 694, 658
MIDDLE_CARD_X, MIDDLE_CARD_Y = 970, 524
POTIONS_X, POTIONS_Y = 273, 1014
QUEST_TEXT_BOX = (722, 975, 72, 29)
PASS_TEXT_BOX = (654, 645, 93, 35)
EXIT_X, EXIT_Y = 499, 1032
QUIT_X, QUIT_Y = 715, 853
WIZ_ICON_X, WIZ_ICON_Y = 1157, 1060

potions = 3

def capture_screen(region=None):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def filter_yellow_text(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Define the range for yellow color
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result

def extract_text_with_coordinates(image):
    filtered_image = filter_yellow_text(image)
    # Debug: Save the filtered image to check if yellow text is correctly isolated
    # cv2.imwrite('filtered_image.png', filtered_image)

    gray = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
    results = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    # Debug: Print OCR results
    # print("OCR Results:", results['text'])

    for i in range(len(results['text'])):
        if "rank" in results['text'][i].lower():
            x, y, w, h = results['left'][i], results['top'][i], results['width'][i], results['height'][i]
            # print(f"x={x}, y={y}, w={w}, h={h}")
            return (x + w//2, y + h//2)  # Return the center of the bounding box
    return None

def text_exists(image, text, region=None):
    if region:
        x,y,w,h = region
        image = image[y:y+h, x:x+w]

    filtered_image = filter_yellow_text(image)
    gray = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
    results = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    for i in range(len(results['text'])):
        if text in results['text'][i].lower():
            return True
    return False

def find_template(image, template_path, threshold=0.9):
    template = cv2.imread(template_path, 0)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):  # Switch columns and rows
        return pt
    return None

def press_key(key, duration=0.1):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def turn_left(duration=0.1):
    press_key('a', duration)

def turn_right(duration=0.1):
    press_key('d', duration)

def move_forward(duration=0.1):
    press_key('w', duration)

def move_backward(duration=0.1):
    press_key('s', duration)

def jump(duration=0.01):
    press_key('space', duration)

def search(screen, warrior_location=None):
    
    screen_width, screen_height = pyautogui.size()
    screen_center_x, screen_center_y = screen_width // 2, screen_height // 2
    offset = +75

    click_at(screen_center_x, screen_center_y)
    pyautogui.mouseDown()

    none_found = 0
    none_max = 40

    while (warrior_location == None):
        print("Troubled Warrior not found...")
        pyautogui.move(offset, 0)
        screen = capture_screen((0, 0, 1919, 449))
        warrior_location = extract_text_with_coordinates(screen)

        none_found += 1
        if none_found > none_max:
            cv2.imwrite('nothing_found.png', screen)
            print("Nothing has been found for a while, clipping, clicking wiz icon and moving character.")

            click_at(WIZ_ICON_X, WIZ_ICON_Y)
            time.sleep(1)

            move_forward(random.randint(3,10)/5)
            move_backward(random.randint(3,10)/5)
            pyautogui.drag(100, 0, random.randint(3, 10)/5, button='right')
            
            clip()

            time.sleep(3)
            none_found = 0

    print("Troubled Warrior found at:", warrior_location)
    warrior_x, warrior_y = warrior_location
    x_diff = warrior_x - screen_center_x
    print(f"x_diff is {x_diff}, x_diff/50={x_diff/50}")
    pyautogui.mouseUp()
    time.sleep(0.01)

    pyautogui.drag(x_diff/20, 0, random.randint(3, 10)/25, button='right')
    pyautogui.drag(2, 30, 0.2, button='right')
    
    move_forward(random.randint(14,20)/8)

def move_to_location(x, y):
    screen_width, screen_height = pyautogui.size()
    screen_center_x = screen_width // 2
    x_diff = abs(x - screen_center_x)
    print(f"x_diff = {x_diff}")

    # Target in middle of screen
    # if x_diff < 180:
    #     move_forward(random.randint(10, 20) / 10)
    #     return

    # if x > screen_center_x:
    #     turn_right(random.randint(2, 4) / 10 * (x_diff/1000))
    #     move_forward(random.randint(10, 20) / 10)
        
    # elif x < screen_center_x:
    #     turn_left(random.randint(2, 4) / 10 * (x_diff/1000))
    #     move_forward(random.randint(10, 20) / 10)

def click_at(x, y):
    time.sleep(.5)
    pyautogui.moveTo(x, y)
    pyautogui.click()
        
def engage_combat():
    no_pass = 0

    while True:
        time.sleep(2)

        # combat_screen = capture_screen((0, 0, 1919, 600))
        # cv2.imwrite('combat_screen.png', combat_screen)
        text_screen = capture_screen(QUEST_TEXT_BOX)
        pass_screen = capture_screen(PASS_TEXT_BOX)
        # cv2.imwrite('pass_text.png', pass_screen)

        if text_exists(text_screen, "defeat"):
            print("Combat ended. Checking mana.")
            check_mana()

            decision = random.randint(1,3)
            movement = random.randint(40,60)
            if (decision == 1):
                pyautogui.drag(movement, 0, random.randint(3, 10)/20, button='right')
                pyautogui.drag(-movement-10, 0, random.randint(3, 10)/20, button='right')
            if (decision == 2):
                pyautogui.drag(-movement, 0, random.randint(3, 10)/20, button='right')
                pyautogui.drag(movement-10, 0, random.randint(3, 10)/20, button='right')
            if (decision == 3):
                jump()

            move_forward(random.randint(3,10)/10)
            move_backward(random.randint(3,10)/10)
            move_forward(random.randint(3,10)/10)
            move_backward(random.randint(3,10)/10)

            time.sleep(1.2)

            return

        # Can choose action
        if find_template(pass_screen, "images\pass_text.png"):
            click_at(MIDDLE_CARD_X, MIDDLE_CARD_Y)
            click_at(MIDDLE_CARD_X, MIDDLE_CARD_Y)
            click_at(MIDDLE_CARD_X, MIDDLE_CARD_Y)
            time.sleep(0.1)
            click_at(PASS_BUTTON_X, PASS_BUTTON_Y)
            click_at(MIDDLE_CARD_X, MIDDLE_CARD_Y)
        print("No pass found.")
        no_pass += 1
        if no_pass >= 50:
            print("Wizard101 might be closed, clicking wiz icon.")
            click_at(WIZ_ICON_X, WIZ_ICON_Y)
            time.sleep(3)
            no_pass = 0

        # playable_card_location = find_template(combat_screen, PLAYABLE_CARD_TEMPLATE_PATH, threshold=0.973)
        # if playable_card_location:
        #     print("Playable card found at:", playable_card_location)
        #     click_at(playable_card_location[0], playable_card_location[1])
        #     continue
        # else:
        #     print("No playable card found, choosing PASS")
        #     click_at(PASS_BUTTON_X, PASS_BUTTON_Y)

        time.sleep(1)  # Delay between actions

def check_mana():
    global potions

    print("Checking health and mana...")
    mana_screen = capture_screen((123, 972, 75, 48))
    filtered = filter_yellow_text(mana_screen)
    # cv2.imwrite('filtered_mana.png', filtered)
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    try:
        mana = int(pytesseract.image_to_string(gray, config='--psm 6'))
    except ValueError:
        return

    print(f"Current mana is {mana}.")

    if mana <= 10:
        click_at(POTIONS_X, POTIONS_Y)
        potions -= 1
        time.sleep(0.2)
        click_at(960, 450)

def clip():
    pyautogui.keyDown('alt')
    time.sleep(0.1)
    pyautogui.press('f10')
    time.sleep(0.1)
    pyautogui.keyUp('alt')

def main():
    global potions

    while potions >= 0:
        screen = capture_screen((0, 0, 1919, 449))
        text_screen = capture_screen(QUEST_TEXT_BOX)
        # Debug: Save the screenshot to verify quality
        # cv2.imwrite('screenshot.png', screen)

        warrior_location = extract_text_with_coordinates(screen)
        quest_exists = text_exists(text_screen, "defeat")

        if not quest_exists:
            print("Quest Text not found, engaging combat.")
            # time.sleep(2)
            engage_combat()
            continue

        search(screen, warrior_location)

        # if warrior_location:
        #     print("Troubled Warrior found at:", warrior_location)
        #     search(screen, warrior_location)
        # else:
        #     print("Troubled Warrior not found...")
        #     # Spin until Troubled Warrior is found
        #     # turn_left(random.randint(3, 10) / 10)
        #     search(screen)
        
        # time.sleep(0.1)  # Add delay to prevent excessive CPU usage
    
    print("Out of potions and mana, clipping and exitting W101.")

    click_at(1605, 974)
    time.sleep(13)
    pyautogui.press('escape')
    time.sleep(1)
    click_at(QUIT_X, QUIT_Y)
    time.sleep(13)
    click_at(EXIT_X, EXIT_Y)
    time.sleep(13)

    clip()

if __name__ == "__main__":
    main()