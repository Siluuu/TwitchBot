import os
import shutil
import app.logging as log


def try_print(text):
    try:
        print(text)
    except:
        pass

# prints the text centered on the console
def print_centered(text):
    columns, _ = shutil.get_terminal_size()

    padding = (columns - len(text)) // 2

    centerd = " " * padding + text
    log.logger.info(centerd)
    try_print(centerd)


# Clear screen 
os.system('cls' if os.name == 'nt' else 'clear')


def first_print():
    first_print = '╔══════════════════════════════════╗'

    try_print('\n')
    first_print = print_centered(first_print)


def rewards_are_ready():
    rewards_are_ready = '║        Rewards are ready!        ║'

    rewards_are_ready = print_centered(rewards_are_ready)


def watchtime_are_ready():
    watchtime_are_ready = '║       Watchtime are ready!       ║'

    watchtime_are_ready = print_centered(watchtime_are_ready)


def twitch_chatbot_ready(bot_name):
    twitch_chatbot_ready = f'║ Logged in as {bot_name} ║'

    twitch_chatbot_ready = print_centered(twitch_chatbot_ready)


def last_print():
    last_print = '╚══════════════════════════════════╝'

    last_print = print_centered(last_print)
    try_print('\n\n\n')


def test_prints(bot_name):
    first_print()
    rewards_are_ready()
    watchtime_are_ready()
    twitch_chatbot_ready(bot_name)
    last_print()




if __name__ == '__main__':
    test_prints(bot_name='Bot Name')
    input()
