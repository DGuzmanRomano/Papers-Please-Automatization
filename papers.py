import cv2
import pytesseract
import pyautogui
import time
import numpy as np
import os




def read_image(image_path):
    # Path to the Tesseract OCR executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    scale_percent = 250
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(gray, dim, interpolation=cv2.INTER_LINEAR)

    # Apply thresholding to improve OCR accuracy for pixel art fonts
    _, thresh = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Configure Tesseract OCR engine for pixel art fonts
    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,' 

    # Perform OCR on the thresholded image
    text = pytesseract.image_to_string(thresh, config=config)

    # Print the extracted text
    print(text)

def click(x, y):
    # Move to the specified screen coordinates and click
    pyautogui.moveTo(x, y)
    pyautogui.click()

    # Print confirmation message
    print(f"Clicked at ({x}, {y})")

def drag_and_drop(start_x, start_y, end_x, end_y):
    # Move the mouse to the starting position and press the mouse down
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()

    # Optionally add a slight delay to ensure the mouse down event is registered
    time.sleep(0.2)

    # Drag the mouse to the ending position (while holding the button down)
    pyautogui.moveTo(end_x, end_y, duration=0.1)  # Duration of the drag

    # Release the mouse button to drop
    pyautogui.mouseUp()

    # Print confirmation message
    print(f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")



def wait_passport():
    # The region to capture (left, top, width, height)
    region = (250, 748, 152, 121)  # Adjust these values to your specific region
    # Path to the desk image
    desk_image_path = r'c:\Users\koopa\Downloads\stacking\PapersPlease\desk.png'
    # Loop until the images do not match
    match_threshold = 0.8  # Adjust the threshold as needed
    while True:
        match_value = compare_to_desk(desk_image_path, region)
        print(f"Match value: {match_value}")
        if match_value < match_threshold:
            print("No match found, exiting loop.")
            break
        else:
            print("Match found, continuing...")
            time.sleep(0.5)  # Wait a bit before retrying






def compare_to_desk(desk_image_path, region):
    # Take a screenshot of the specified region
    screenshot = pyautogui.screenshot(region=region)
    screenshot_img = np.array(screenshot)
    screenshot.save('saved.png')  
    screenshot_gray = cv2.cvtColor(screenshot_img, cv2.COLOR_BGR2GRAY)

    # Load the desk image and convert it to grayscale
    desk_img = cv2.imread(desk_image_path)
    desk_gray = cv2.cvtColor(desk_img, cv2.COLOR_BGR2GRAY)

    # Compare the images
    result = cv2.matchTemplate(screenshot_gray, desk_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val

def screenshotPassport():
    region2 = (250, 748, 152, 121)
    screenshot = pyautogui.screenshot(region=region2)
    
    # Generate a unique filename using the current timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    save_path = os.path.join(r'c:\Users\koopa\Downloads\stacking\PapersPlease', filename)
    
    screenshot.save(save_path)
    print(f"Screenshot saved to {save_path}")


def screenshot_does_not_match(screenshot, image_paths, threshold=0.8):
    screenshot_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    
    for image_path in image_paths:
        comparison_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if comparison_image is None:
            print(f"Error loading image {image_path}")
            continue

        result = cv2.matchTemplate(screenshot_img, comparison_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        if max_val >= threshold:
            # A match is found if max_val is greater than or equal to the threshold
            return False  # The screenshot matches one of the images

    return True  # No matches found



def only_arstotska():
    
    # Define the region for the screenshot
    region = (250, 748, 152, 121)
    screenshot = pyautogui.screenshot(region=region)

    # Absolute image paths to compare
    image_paths = [
        r'c:\Users\koopa\Downloads\stacking\PapersPlease\ars1.png',
        r'c:\Users\koopa\Downloads\stacking\PapersPlease\ars2.png',
        r'c:\Users\koopa\Downloads\stacking\PapersPlease\ars3.png',
        r'c:\Users\koopa\Downloads\stacking\PapersPlease\ars4.png',
        r'c:\Users\koopa\Downloads\stacking\PapersPlease\ars5.png',
        r'c:\Users\koopa\Downloads\stacking\PapersPlease\ars6.png',
        r'c:\Users\koopa\Downloads\stacking\PapersPlease\ars7.png',
        r'c:\Users\koopa\Downloads\stacking\PapersPlease\ars8.png',
        r'c:\Users\koopa\Downloads\stacking\PapersPlease\ars9.png'
    ]
   
    # Check if the screenshot does not match any of the images
    does_not_match = screenshot_does_not_match(screenshot, image_paths, threshold=0.7)
    print(f"The screenshot does not match any of the images: {does_not_match}")
    return does_not_match


def find_image_on_screen(image_path):
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=0.7)
        return location is not None
    except pyautogui.ImageNotFoundException:
        return False



def reject():

    drag_and_drop(337, 808, 1231, 704)
    click(1837, 534)
    time.sleep(0.5)
    click(1217, 514)
    drag_and_drop(1231, 704,338,590)
    click(1837, 534)


def acept():
    drag_and_drop(337, 808, 1623, 697)
    click(1837, 534)
    time.sleep(0.5)
    click(1604, 515)
    drag_and_drop(1623, 697,338,590)
    click(1837, 534)


def wait_speaker():
    image_path = r'c:\Users\koopa\Downloads\stacking\PapersPlease\speakeractivated.png'

    # Loop until the image is found on the screen
    while True:
        image_found = find_image_on_screen(image_path)
        print("Searching for image...")
        if image_found:
            print("Image found on screen.")
            break
        else:
            time.sleep(0.3)  # Wait a bit before retrying to avoid high CPU usage

# Example usage:exampe of use of 
# Wait for a moment before starting 

#day one 
def day_one():
        
    while True:
        # Perform a click action
        wait_speaker()
        click(608, 270)
        time.sleep(0.2)
        wait_passport()
        # Perform a drag and drop action
        screenshotPassport()
        time.sleep(0.2)
        if only_arstotska():
            reject()
            
        else:
            acept()


#day_one()

wait_speaker()
click(608, 270)
time.sleep(0.2)
wait_passport()
# Perform a drag and drop action
screenshotPassport()
time.sleep(0.2)

if only_arstotska():
    reject()
            
else:
    acept()