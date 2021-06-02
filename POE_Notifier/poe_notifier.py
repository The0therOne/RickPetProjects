# Path of Exile PM and TRADE notification.
# You can be AFK and still receive message with PM or TRADE text
# to your messenger (Telegram with your bot or you can change my code for another messenger,
# or smart watch for example)
# by Ricrawl


import time
import subprocess
import telegram_send


class PoeNotifier:
    temp_last_line = ''
    last_line = ''
    active = False
    path_to_watch = "\\Client.txt"  # path to "PathOfExile/Logs/Clients.txt"

    def __init__(self, mode):  # mode = ['PM', 'TRADE']
        self.mode = mode

    def start(self):
        print(f"[+]Starting {self.mode} mode after 5 seconds...")
        time.sleep(5)
        print(f"[+]{self.mode} mode started...")
        self.active = True
        self.last_line = self.get_last_line()
        print(self.last_line)
        print("-" * 50)
        self.send_notify_to_telegram(self.last_line)
        self.temp_last_line = self.last_line
        self.wait_messages(self.last_line, self.temp_last_line)

    def wait_messages(self, last_line, temp_last_line=''):
        try:
            while self.active:
                time.sleep(1)
                if self.mode == 'PM':
                    if last_line != temp_last_line:
                        if '@From' in last_line:
                            print(last_line)
                            self.send_notify_to_telegram(last_line)
                            print("-" * 50)
                            temp_last_line = last_line
                    else:
                        last_line = self.get_last_line()
                elif self.mode == 'TRADE':
                    if last_line != temp_last_line:
                        if '$' in last_line:
                            print(last_line)
                            self.send_notify_to_telegram(last_line)
                            print("-" * 50)
                            temp_last_line = last_line
        except KeyboardInterrupt:
            self.stop()

    def get_last_line(self):
        mode = self.mode
        while True:
            with open(self.path_to_watch, mode='r', encoding='utf-8') as client_f:
                lines = client_f.readlines()
                last_line = lines[len(lines) - 1]
                if mode == 'PM':
                    if '@From' in last_line:
                        return last_line
                    else:
                        continue
                elif mode == 'TRADE':
                    if '$' in last_line:
                        return last_line
                    else:
                        continue

    @staticmethod
    def send_notify_to_telegram(last_line):
        telegram_send.send(messages=[last_line])

    def stop(self):
        self.active = False
        print("[!]Poe_Notifier is closed!")


def main():
    try:
        while True:
            print("""\t\t[1] - start a PM mode\n\t\t
                [2] - start a TRADE mode\n
                [3] - configure a telegram-send module\n
                [4] - exit\n""")
            choose = int(input("Choose the option: "))
            if choose == 1:
                PoeNotifier(mode='PM').start()
            elif choose == 2:
                print("[?]TRADE mode will be added later")
                # PoeNotifier(mode='TRADE').start()
                continue
            elif choose == 3:
                subprocess.call(["telegram-send", "--configure"])
                continue
            elif choose == 4:
                break
            else:
                print("[-]Wrong input, try again!")
                continue
    except ValueError:
        print("[-]Wrong type! Please enter 1, 2, 3, and etc.")
    except KeyboardInterrupt:
        print("[!]Exiting program...")


if __name__ == '__main__':
    main()
