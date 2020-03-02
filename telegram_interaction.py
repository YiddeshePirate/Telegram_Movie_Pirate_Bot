import requests
from threading import Thread
import time
import ytsbot
import os

telegram_key = os.environ.get('TELEGRAM_KEY')
print(telegram_key)
url = f"https://api.telegram.org/bot{telegram_key}"


def send_message(chat_id, message_text):
    message_url = f"{url}/sendMessage?chat_id={chat_id}&text={message_text}"
    requests.post(message_url)


def updating_message():
    global updatepage
    global latest_message
    global latestfrom
    global latestupdateid
    while True:
        time.sleep(0.05)
        updatepage = requests.get(url + "/getUpdates?offset=-1")
        updatepage = updatepage.json()
        latest_message = updatepage["result"][0]["message"]["text"]
        latestfrom = updatepage["result"][0]["message"]["from"]["id"]
        latestupdateid = updatepage["result"][0]["update_id"]


t1 = Thread(target=updating_message)
t1.start()





def wait_for_message(instance, timeout=180):
    global updatepage
    old_message_id = latestupdateid
    print("waiting")
    start_time = time.perf_counter()
    while (
        old_message_id == latestupdateid and time.perf_counter() - start_time < timeout
    ):
        pass
    if time.perf_counter() - start_time > timeout:
        return None

    if latestfrom == instance.chat_id:
        print("test69")
        return updatepage["result"][0]["message"]["text"]
    else:
        instance.nm = instance.wait_for_response()


sessions = []


def lookforstart():
    time.sleep(3)
    while True:
        time.sleep(0.005)
        if latest_message == "/start" and latestfrom not in sessions:

            sessions.append(latestfrom)
            x = request(latestfrom)
            x.startthread()



class request:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.running = True

    def startthread(self):
        self.thread = Thread(target=self.interaction)
        self.thread.start()

    def terminate(self):
        sessions.remove(self.chat_id)

    def wait_for_response(self, timeout=120):
        global updatepage
        old_message_id = latestupdateid

        start_time = time.perf_counter()
        while (
            (old_message_id == latestupdateid) or latestfrom != self.chat_id
        ) and time.perf_counter() - start_time < timeout:
            pass
        self.nm = latest_message

    def wait_for_response_thread(self):
        self.responsethread = Thread(target=self.wait_for_response)
        self.responsethread.start()

    def send_chat_message(self, message):
        send_message(self.chat_id, message)

    def get_suggestions(self, search_term):
        self.suggestions = ytsbot.Movie_suggestions(
            ytsbot.get_search_links_ai(search_term)
        )

    def set_movie(self, number):
        self.movie = ytsbot.Movie(self.suggestions.joined_list[int(number)])

    def download_movie(self, quality):
        self.movie.download_from_magnet(quality)

    def wait_while_downloading(self):
        self.movie.get_progress()
        while self.movie.percent < 100:
            self.wait_for_response()
            if not self.nm:
                pass
            elif "status" in self.nm:
                self.movie.get_progress()
                self.send_chat_message(self.movie.waiting_message)
            else:
                pass

    def interaction(self):
        try:
            self.send_chat_message("Enter search term")
            self.wait_for_response()
            self.get_suggestions(self.nm)
            self.send_chat_message(self.suggestions.list_of_options)
            self.send_chat_message("Select From Options")
            self.wait_for_response()
            self.set_movie(self.nm)
            self.send_chat_message("Select quality")
            self.wait_for_response()
            self.download_movie(self.nm)
            self.wait_while_downloading()
            self.send_chat_message("Done!")
            self.terminate()
            return 0
        except:
            self.send_chat_message("Something went wrong")
            self.terminate()
            return 1

lookforstart()
