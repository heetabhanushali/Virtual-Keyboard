import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from PIL import ImageDraw, ImageFont, Image
import numpy as np

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand detector
detector = HandDetector(detectionCon=0.8)

# Keyboard layouts
keys_alpha = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["⇪", "A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", "Delete"],
    ["123", "#@!", "Space"]
]

keys_numeric = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["-", "/", ":", ";", "(", ")", "$", "&", "@", "\""],
    [".", ",", "?", "!", "'", "Delete"],
    ["ABC", "#@!", "Space"]
]

keys_special = [
    ["[", "]", "{", "}", "#", "%", "^", "*", "+", "="],
    ["_", "\\", "|", "~", "<", ">", "€", "£", "¥", "•"],
    ["←", "→", "↑", "↓", "Delete"],
    ["ABC", "123", "Space"]
]

mode = "alpha"
caps = False
finaltext = ""

# Button class with image caching
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size
        self.img_cache = {}
        for cap in [False, True]:
            for state in ['normal', 'hover', 'click']:
                self.img_cache[(cap, state)] = self.create_img(cap, state)

    def create_img(self, caps, state):
        w, h = self.size
        colors = {'normal': (255, 0, 255), 'hover': (0, 0, 255), 'click': (175, 0, 175)}
        bcolor = colors[state]

        img_pil = Image.new("RGB", (w, h), bcolor)
        draw = ImageDraw.Draw(img_pil)
        try:
            font = ImageFont.truetype("Arial Unicode.ttf", 40)
        except:
            font = ImageFont.load_default()

        display_text = self.text
        if len(display_text) == 1 and display_text.isalpha():
            display_text = display_text.upper() if caps else display_text.lower()

        bbox = font.getbbox(display_text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (w - text_width) // 2
        text_y = (h - text_height) // 2 - 5

        draw.text((text_x, text_y), display_text, font=font, fill=(255, 255, 255))
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def draw(self, img, caps, state='normal'):
        x, y = self.pos
        w, h = self.size
        btn_img = self.img_cache[(caps, state)]

        alpha = 0.7  # Transparency factor (0 = fully transparent, 1 = fully solid)
        background_roi = img[y:y+h, x:x+w]
        blended = cv2.addWeighted(btn_img, alpha, background_roi, 1 - alpha, 0)
        img[y:y+h, x:x+w] = blended
        return img

# Create keyboard
buttonlist = []
def build_keyboard(layout):
    global buttonlist
    buttonlist = []
    for i in range(len(layout)):
        for j, key in enumerate(layout[i]):
            if key == "Space":
                buttonlist.append(Button([100 * j + 50, 100 * i + 50], key, size=[400, 85]))
            elif key == "Delete":
                buttonlist.append(Button([100 * j + 50, 100 * i + 50], key, size=[285, 85]))
            else:
                buttonlist.append(Button([100 * j + 50, 100 * i + 50], key))

build_keyboard(keys_alpha)

# Main loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    hover_button = None
    click_button = None

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            index_tip = lmList[8][:2]
            thumb_tip = lmList[4][:2]

            for button in buttonlist:
                x, y = button.pos
                w, h = button.size
                if x < index_tip[0] < x + w and y < index_tip[1] < y + h:
                    hover_button = button
                    l, _, _ = detector.findDistance(index_tip, thumb_tip, img)
                    if l < 30:
                        click_button = button
                        break

    for button in buttonlist:
        state = 'normal'
        if button == click_button:
            state = 'click'
        elif button == hover_button:
            state = 'hover'
        img = button.draw(img, caps, state)

    # Placeholder using PIL (displays full finaltext, with left-side cropping if needed)
    x, y, w, h = 50, 600, 1000, 100
    placeholder_img = Image.new("RGB", (w, h), (50, 50, 50))
    draw = ImageDraw.Draw(placeholder_img)
    try:
        font = ImageFont.truetype("Arial Unicode.ttf", 40)
    except:
        font = ImageFont.load_default()

    display_text = finaltext
    while True:
        bbox = font.getbbox(display_text)
        text_width = bbox[2] - bbox[0]
        if text_width <= w - 20 or len(display_text) <= 1:
            break
        display_text = display_text[1:]

    draw.text((10, 30), display_text, font=font, fill=(255, 255, 255))
    placeholder_np = cv2.cvtColor(np.array(placeholder_img), cv2.COLOR_RGB2BGR)
    img[y:y+h, x:x+w] = placeholder_np

    # Handle key press
    if click_button:
        text = click_button.text
        print("Clicked:", text)

        if text == "⇪":
            caps = not caps
            if mode == "alpha":
                build_keyboard(keys_alpha)
        elif text == "123":
            mode = "number"
            build_keyboard(keys_numeric)
        elif text == "#@!":
            mode = "special"
            build_keyboard(keys_special)
        elif text == "ABC":
            mode = "alpha"
            build_keyboard(keys_alpha)
        elif text == "Delete":
            finaltext = finaltext[:-1]
        elif text == "Space":
            finaltext += " "
        else:
            if len(text) == 1 and text.isalpha():
                finaltext += text.upper() if caps else text.lower()
            else:
                finaltext += text
        sleep(0.3)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
