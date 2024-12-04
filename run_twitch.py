import threading
from time import sleep
import app.twitch.oauth_2 as oauth
import app.twitch.twitch_chatbot as twitch_chatbot
import app.twitch.twitch_rewards as rewards
import app.twitch.watchtime as watchtime
import app.twitch.request as request
import app.twitch.minigame as minigame

def start_bot():
    thread0 = threading.Thread(target=oauth.setup)
    thread1 = threading.Thread(target=twitch_chatbot.twitch_chatbot_start)
    thread2 = threading.Thread(target=rewards.twitch_rewards_start)
    thread3 = threading.Thread(target=watchtime.set_watchtime)
    thread4 = threading.Thread(target=minigame.setup)

    thread0.start()
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread0.join()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()



if __name__ == '__main__':
    oauth.Oauth().validate_token()
    sleep(2)
    start_bot()
