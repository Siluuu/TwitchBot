import os
import json
import datetime
from time import sleep
import app.twitch.request as request
import app.style.better_print as better_print
import app.logging as log
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CHANNEL_NAME = os.getenv('TWITCH_CHANNEL_NAME')
CHATBOT_NAME = os.getenv('TWITCH_CHATBOT_NAME')

filename = 'json/twitch/watchtime.json'


# Counts the Watchtime for Followers that are watching the stream live
def set_watchtime():
    better_print.first_print()
    better_print.watchtime_are_ready()
    while True:
        try:
            is_live = request.get_streams()
            try:
                with open(filename, 'r') as save_file:
                    save_watchtime = json.load(save_file)
            except FileNotFoundError:
                save_watchtime = {}

            if is_live == True:
                chatters = request.get_channel_chatters()
                follower = request.get_channel_followers()

                blacklist = [f'{CHANNEL_NAME.lower()}', f'{CHATBOT_NAME.lower()}', 'coopcompanion']

                for viewer in chatters:
                    if viewer in save_watchtime:
                        if viewer in follower and viewer not in blacklist:
                            save_watchtime[viewer] += 1
                        else:
                            pass
                    else:
                        save_watchtime[viewer] = 0

                with open(filename, 'w') as save_file:
                    json.dump(save_watchtime, save_file, indent=4)

                time = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                #print(time)
                sleep(0.002)
            else:
                #print(f'{CHANNEL_NAME} ist nicht live.')
                sleep(10)
        except Exception as err:
            #oauth.validate_token()
            error = f'[Twitch Watchtime] Error in set_watchlist: {err}'
            log.log_error(error)


# returns the watchtime from a follower
def get_watchtime(username):
    try:
        username = str(username).lower()
        #print(f'Username: {username}')
        with open(filename, 'r') as save_file:
            save_watchtime = json.load(save_file)
            #print(f'Save watchtime: {save_watchtime}')
            watchtime = save_watchtime[username]
            watchtime = time_converter(int(watchtime))
            #print(f'{watchtime}\n')

        return watchtime
    except Exception as err:
        error = f'[Twitch Watchtime] Error in get_watchtime: {err}'
        log.log_error(error)


# return the top five follower with the most watchtime
def get_watchtime_leaderboard():
    try:
        try:
            with open(filename, 'r') as save_file:
                save_watchtime = json.load(save_file)
        except:
            return 'watchlist konnte nicht gefunden werden. NotLikeThis'

        top_watchtime = sorted(save_watchtime.items(), key=lambda x: x[1], reverse=True)[:5]

        top_watchtime_list = []
        top_watchtime_count = 0

        for viewer, watchtime in top_watchtime:
            top_watchtime_count += 1
            watchtime = time_converter(watchtime)
            top_watchtime_list.append(f'#{top_watchtime_count} @{viewer} mit {watchtime}')

        top_5_watchtime = f'{top_watchtime_list[0]}, {top_watchtime_list[1]}, {top_watchtime_list[2]}, {top_watchtime_list[3]}, {top_watchtime_list[4]}'
        #print(top_5_watchtime)
        
        return top_5_watchtime

    except Exception as err:
        error = f'[Twitch Watchtime] Error in get_watchtime_leaderboard: {err}'
        log.log_error(error)


# converts the watchtime from seconds up to days
def time_converter(duration_in_seconds):
    try:
        minutes, seconds = divmod(duration_in_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        watchtime = {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }

        seconds = watchtime['seconds']
        minutes = watchtime['minutes']
        hours = watchtime['hours']
        days = watchtime['days']

        if days == 0:
            if hours == 0:
                if minutes == 0:
                    if seconds == 0:
                        #watchtime = (f'Ẽ̸̯͎͕̰͊̑͋̔̆̐͗́̇̇̊͛͘͠͠r̴̛̩̩̔̉͆͊̌̈́̂̉̃̀̂͘͝͠͝r̷̨̼͔̹͛̇͂͝ő̶͖̺̗̙̲̓͜͜͝r̷̡̡̘͖͓̻̿̐͆̇̌̂̑̀̏̿ͅ  {seconds}s (つ◉益◉)つ')
                        watchtime = (f'Ẽ̸̯͎͕̰͊̑͋̔̆̐͗́̇̇̊͛͘͠͠r̴̛̩̩̔̉͆͊̌̈́̂̉̃̀̂͘͝͠͝r̷̨̼͔̹͛̇͂͝ő̶͖̺̗̙̲̓͜͜͝r̷̡̡̘͖͓̻̿̐͆̇̌̂̑̀̏̿ͅ ')
                    else:
                        watchtime = (f'{seconds}s')
                else:
                    watchtime = (f'{minutes}min und {seconds}s')
            else:
                watchtime = (f'{hours}h {minutes}min und {seconds}s')
        else:
            watchtime = (f'{days}d {hours}h {minutes}min und {seconds}s')

        return watchtime
    
    except Exception as err:
        error = f'[Twitch Watchtime] Error in time_converter: {err}'
        log.log_error(error)





if __name__ == '__main__':
    #set_watchtime()
    #get_watchtime('username')
    get_watchtime_leaderboard()
