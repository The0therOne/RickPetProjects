import time
import webbrowser
import random


class AlarmClock:
    YouTubeUrls = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ",]

    def __init__(self, sec):
        self.sec = int(sec)
        self.url = ''

    def get_random_url(self):
        self.url = random.choice(self.YouTubeUrls)
        return self.url

    def start_alarm(self):
        print(f"{self.sec} seconds left...")
        while self.sec > 0:
            time.sleep(1)
            self.sec -= 1
            print(f"{self.sec} seconds left...")
        self.end_alarm()

    def end_alarm(self):
        print(f"Time to watch videos!\n" * 3)
        webbrowser.open(self.get_random_url(), new=2)


def main():
    print("Hello. Welcome to my WakeUpWithYouTube.")
    seconds = input("Enter when to wake up (in seconds): ")
    alarm_clock = AlarmClock(seconds)
    alarm_clock.start_alarm()


main()
