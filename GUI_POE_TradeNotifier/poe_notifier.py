import time
import telegram_send
from subprocess import run, PIPE


class PoeNotifier:
    """
    Class for PoeNotifier script
    """
    active = False
    path_to_watch = ""

    def __init__(self, mode="pm"):
        self.mode = mode

    def start(self):
        """
        Method for init first start of script and printing last line in Client.txt
        :return:
        """
        time.sleep(1)
        print(f"[+]{self.mode} mode started...")
        self.active = True
        last_line = self.get_last_line()
        if last_line is not None:
            temp_last_line = last_line
            print(last_line)
            print("-" * 50)
            self.send_notify_to_telegram(last_line)
            self.wait_messages(last_line, temp_last_line)

    def wait_messages(self, last_line, temp_last_line):
        """
        Method for waiting messages from game to check them and send message to telegram
        :param last_line:
        :param temp_last_line:
        :return:
        """
        while self.active:
            time.sleep(1)
            if self.mode == 'pm':
                if last_line != temp_last_line:
                    if '@From' in last_line:
                        print(last_line)
                        print("-" * 50)
                        self.send_notify_to_telegram(last_line)
                        temp_last_line = last_line
                else:
                    last_line = self.get_last_line()
            elif self.mode == 'trade':
                if last_line != temp_last_line:
                    if '$' in last_line:
                        print(last_line)
                        print("-" * 50)
                        self.send_notify_to_telegram(last_line)
                        temp_last_line = last_line
                else:
                    last_line = self.get_last_line()

    def get_last_line(self):
        """
        Function for getting last line in Client.txt file
        :return:
        """
        while self.active:
            with open(self.path_to_watch, mode='r', encoding='utf-8') as client_f:
                lines = client_f.readlines()
                last_line = lines[len(lines) - 1]
                if self.mode == 'pm':
                    if '@From' in last_line:
                        return last_line
                elif self.mode == 'trade':
                    if '$' in last_line:
                        return last_line

    def send_notify_to_telegram(self, last_line):
        """
        Sending last line from Client.txt to telegram bot
        :param last_line:
        :return:
        """
        if self.mode == 'pm':
            telegram_send.send(messages=[last_line.split('@')[1]])
        elif self.mode == 'trade':
            telegram_send.send(messages=[last_line.split('$')[1]])

    def stop(self):
        """
        Stop monitoring Client.txt
        :return:
        """
        print('Notifier has stopped!')
        self.active = False
