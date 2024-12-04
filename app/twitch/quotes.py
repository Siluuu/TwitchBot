import json
import random
import datetime
import app.twitch.request as request
import app.logging as log
import app.style.better_print as better_print

filename = 'json/shared/quotes.json'

# saves the quote that was added from a twitch moderator or the channel owner
def save_quotes(new_quote):
    global quote_added
    time = datetime.datetime.now().strftime('%H:%M:%S')
    try:
        try:
            with open(filename, 'r') as save_file:
                saved_quotes = json.load(save_file)
        except FileNotFoundError:
            saved_quotes = {}

        #Höchste Quote number +1
        next_key = str(max(map(int, saved_quotes.keys()), default=0) + 1)
        game_name = request.get_channel_info()
        new_quote = f'{new_quote} {game_name}'

        #Fügt die neue Quote hinzu
        saved_quotes[next_key] = new_quote

        #Speichert die Quote in quotes.json
        with open(filename, 'w') as save_file:
            json.dump(saved_quotes, save_file, indent=4)

        quote_added = f'Quote #{next_key} hinzugefügt.'
        better_print.try_print(f'{time} - {quote_added}\n')
        
    except Exception as err:
        error = f'[Twitch Quotes] Error in save_quotes: {err}'
        log.log_error(error)


# loads the quote that was randomly choosen
def load_quotes():
    global saved_quotes
    global quote_key
    time = datetime.datetime.now().strftime('%H:%M:%S')
    try:
        with open(filename, 'r') as save_file:
            saved_quotes = json.load(save_file)
        
        if saved_quotes:
            quote_key = random.choice(list(saved_quotes.keys()))
            better_print.try_print(f'{time} - {quote_key}: {saved_quotes[quote_key]}\n')
        else:
            better_print.try_print('No quotes available.\n')

    except FileNotFoundError:
        error = '[Twitch Quotes] No quotes available.\n'
        log.log_error(error)


# removes the quote that was choosen
def remove_quotes(quote_key):
    global quote_removed
    time = datetime.datetime.now().strftime('%H:%M:%S')
    try:
        with open(filename, 'r') as save_file:
            saved_quotes = json.load(save_file)

        if quote_key in saved_quotes:
            removed_quote = saved_quotes.pop(quote_key)

            for i, key in enumerate(sorted(saved_quotes.keys(), key=int)):
                saved_quotes[str(i + 1)] = saved_quotes.pop(key)

            with open(filename, 'w') as save_file:
                json.dump(saved_quotes, save_file, indent=4)

            quote_removed = f'Quote #{quote_key} entfernt.'
            better_print.try_print(f'{time} - Quote removed: {quote_key}: {removed_quote}\n')
        else:
            better_print.try_print(f'{time} - Quote with key {quote_key} not found.\n')

    except FileNotFoundError:
        error = '[Twitch Quotes] No quotes available.'
        log.log_error(error)


if __name__ == '__main__':
    load_quotes()
