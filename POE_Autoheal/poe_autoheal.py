import time
import cv2
import mss
import numpy as np
import pyautogui


def use_hp_potion():
    pyautogui.keyDown('1')
    time.sleep(0.1)
    pyautogui.keyUp('1')


title = "[POE] Auto-heal"
sct = mss.mss()

print("Starting after 15 seconds...")
time.sleep(15)
print("Started...")

while True:
    mon = {"top": 850, "left": 60, "width": 100, "height": 50} #You need configure it for youself
    img = np.asarray(sct.grab(mon))

    # create hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define masks
    # lower mask(0-10)
    lower_red = np.array([0,200,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,200,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # join masks
    mask = mask0 + mask1

    # check
    hasRed = np.sum(mask)
    if hasRed > 0:
        pass
    else:
        print("Using Health Potion...")
        time.sleep(0.3)
        use_hp_potion()
        time.sleep(2)

    cv2.imshow(title, img)
    if cv2.waitKey(25) & 0xFF == ord("q"):
        print(img)

        cv2.destroyAllWindows()
        quit()
