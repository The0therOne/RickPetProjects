# Path of Exile PM notification. For trade message.
# You can AFK, but you will receive message with screenshot of PM message...
# to your messenger (Telegram) or smart watch (later)

import time
from datetime import datetime
import cv2
import mss
import numpy as np
import pytesseract

from fuzzywuzzy import fuzz


class PoeNotifier:
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    title = "[POE] PM_Notify"
    sct = None
    config = None

    ocr = {
        "enabled": True,
        "exclude": False,
        "list": []
    }

    active = False

    def __init__(self):
        self.sct = mss.mss()

    def start(self):
        print(f"Starting after 15 seconds...")
        time.sleep(3)
        print("Started...")
        self.active = True
        self.wait_messages()

    def stop(self):
        self.active = False

    def wait_messages(self):
        while self.active:
            # Full chat
            # mon_scr = {"top": 450, "left": 120, "width": 250, "height": 320}
            # "@From" place
            mon_from_place = {"top": 450, "left": 45, "width": 150, "height": 320}
            img = np.asarray(self.sct.grab(mon_from_place))

            # create rgb for tesseract
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # read psm 6 & 7
            pcm3 = pytesseract.image_to_string(rgb, lang='eng', config='--psm 3')
            pcm6 = pytesseract.image_to_string(rgb, lang='eng', config='--psm 6')
            pcm7 = pytesseract.image_to_string(rgb, lang='eng', config='--psm 7')

            self.show(self.title, img)

            if fuzz.ratio(pcm6, f'[12:45] @From') > 20 or fuzz.ratio(pcm7, '[12:45] @From') > 20 or fuzz.ratio(pcm3, '[12:45] @From') > 20:
                print("[+]New PM received!")
            else:
                print(f"[-]{self.current_time}@From")
                # print("[-]No new messages.")c
                time.sleep(2)

    def send_scr_to_telegram(self):
        pass

    def show(self, title, img):
        cv2.imshow(title, img)
        if cv2.waitKey(27) & 0xFF == ord("q"):
            # print(img)

            cv2.destroyAllWindows()
            quit()


bot = PoeNotifier()

bot.start()
