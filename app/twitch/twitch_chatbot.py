import os
import random
import datetime
import json
import asyncio
import app.twitch.quotes as quotes
import app.twitch.request as request
import app.twitch.watchtime as watchtime
import app.twitch.minigame as minigame
import app.style.better_print as better_print
import app.logging as log
from dotenv import load_dotenv
from twitchio.ext import commands
from twitchio.client import Client
from rcon.source import Client

load_dotenv()

CHANNEL_NAME = os.getenv('TWITCH_CHANNEL_NAME')

DISCORD = os.getenv('DISCORD')
STEAM = os.getenv('STEAM')
SOCIALS = os.getenv('SOCIALS')
TTS = os.getenv('TTS')

ARK_SERVER_IP = os.getenv('ARK_SERVER_IP')
ARK_SERVER_PORT = os.getenv('ARK_SERVER_PORT')
ARK_SERVER_PW = os.getenv('ARK_SERVER_PW')

bot = commands.Bot(
    token=os.getenv('TWITCH_OAUTH_TOKEN'),
    client_id=os.getenv('TWITCH_CLIENT_ID'),
    nick=os.getenv('TWITCH_CHATBOT_NAME'),
    prefix='!',
    initial_channels=[CHANNEL_NAME],
)


@bot.event()
async def event_ready():
    better_print.twitch_chatbot_ready(bot.nick)
    better_print.last_print()

    task0 = asyncio.create_task(start_interval(450.0))
    task1 = asyncio.create_task(update_played_games())
    
    await asyncio.gather(task0, task1)


# Starts the interval for the intaval messages
async def start_interval(interval):
    while True:
        try:
            await asyncio.sleep(interval)
            await interval_message()

        except Exception as err:
            error = f'[Twitch Chatbot] Error in start_interval: {err}'
            log.log_error(error)


# sends a interval message
async def interval_message():
    channel = bot.get_channel(CHANNEL_NAME)
    if channel:
        is_live = request.get_streams() 

        if is_live == True:
            filename='json/twitch/count.json'

            try:
                with open(filename, 'r') as save_file:
                    count = json.load(save_file)
            except:
                count = {}

            if count['count'] == 1:
                count['count'] = 2
                await channel.send(f'Hier gehts zum neuen Discord: {DISCORD}')

            elif count['count'] == 2:
                count['count'] = 3
                await channel.send(f'Die Anleitung für TTS: {TTS}')

            elif count['count'] == 3:
                count['count'] = 1
                await channel.send(f'Um Rollen in Discord zu erhalten löse Channelpoints: Discord Rollen ein. (Beschreibung lesen) PogChamp')

            with open(filename, 'w') as save_file:
                json.dump(count, save_file, indent=4)

        else:
            return
        

# loop to get the game name every 10s from the game that is currently played and saves it
async def update_played_games():
    while True:
        if request.get_streams():
            game_name = request.get_channel_info()
            filename = 'json/twitch/pick_game.json'
            with open(filename, 'r') as load_file:
                pick_game_dict = json.load(load_file)
                played_games_dict = pick_game_dict.get('played_games', {})

            played_games_list = []
            
            game_name = game_name.replace('[', '').replace(']', '')

            try:
                for key in played_games_dict.keys():
                    played_game = played_games_dict[key]
                    played_games_list.append(played_game)

                if game_name not in played_games_list:
                    next_key = str(max(map(int, pick_game_dict['played_games'].keys()), default=0) + 1)
                    pick_game_dict['played_games'][next_key] = game_name

                    with open(filename, 'w') as save_file:
                        json.dump(pick_game_dict, save_file, indent=4)

            except:
                pass        

        await asyncio.sleep(10)


@bot.event()
async def event_reconnect():
    log.log_info('[Twitch Chatbot] Reconnecting...')

@bot.event()
async def event_token_expired():
    log.log_error('[Twitch Chatbot] Token expired. Please refresh the token.')
    return None

@bot.event()
async def event_error(err):
    error = f'[Twitch Chatbot] Error catched by event_error: {err}'
    log.log_error(error)


# shows messages, that was send in the twitch chat
@bot.event()
async def event_message(message):
    try:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        
        if message.author:
            viewer = message.author.name
        else:
            viewer = bot.nick

        message = message.content

        full_message = f'{time} - [Twitch] {viewer}: {message}'
        log.log_info(full_message)

    except Exception as err:
        error = f'[Twitch Chatbot] Error in event_message: {err}'
        log.log_error(error)


#Failed Commands
@bot.command(name='active')
async def active(ctx):
    ark_server_message = f'twitch.tv/louisderlauch'
    try:
        async with Client(ARK_SERVER_IP, int(ARK_SERVER_PORT), passwd=ARK_SERVER_PW) as client:
            response1 = client.run(str('ListPlayers'))
            #response2 = client.run(str(f'SetMessageofTheDay {ark_server_message}'))
            better_print.try_print(f'{response1}\n')
            response1 = "".join([i for i in response1 if not i.isdigit()])
            better_print.try_print(response1)
            await ctx.send(f'{response1}')

    except Exception as err:
        await ctx.send('Der Ark Server ist gerade nicht Online oder nicht erreichbar.')
        error = f'[Twitch Chatbot] error in active: {err}'
        log.log_error(error)



# Chat Commands | sends links to the twitch chat
@bot.command(name='dc', aliases=['discord'])
async def Discord(ctx):
    await ctx.send(f'@{ctx.author.name} hier gehts zum neuen Discord: {DISCORD}')

@bot.command(name='steam')
async def Steam(ctx):
    await ctx.send(f'@{ctx.author.name} mein Steam: {STEAM}')
    
@bot.command(name='social', aliases=['socials'])
async def Socials(ctx):
    await ctx.send(f'@{ctx.author.name} hier sind meine Socials: {SOCIALS}')

@bot.command(name='tts')
async def Tts(ctx):
    await ctx.send(f'Die Anleitung für TTS: {TTS}')

@bot.command(name='lurk')
async def Lurk(ctx):
    await ctx.send(f'@{ctx.author.name} geht in den lurk.')



# 8ball | sends randomly anwsers to a question in the twitch chat
@bot.command(name='8ball', aliases=['magische', 'magischer', 'magisches', 'mmm'])
async def Eightball(ctx):
    eightball_anwser = ['ja', 'nein', 'vllt', 'wahrscheinlich', 'unwahrscheinlich', 'in der Tat Kappa', 'Für Fortnite!']
    eightball = random.choice(eightball_anwser)
    await ctx.send(f'@{ctx.author.name} {eightball}')



# Chat Interaction Commands
# adding a quote with that was send by a moderator or by the channel owner
@bot.command(name='addquote')
async def AddQuote(ctx):
    viewer = ctx.author.name
    modlist = request.get_moderators()
    if viewer in modlist or viewer == CHANNEL_NAME:
        message = ctx.message.content
        _, new_quote = message.split(' ', 1)

        quotes.save_quotes(new_quote)
        await ctx.send(f'{quotes.quote_added}')
    else:
        await ctx.send(f'@{viewer} du hast keine Berechtigung für diesen Befehl. cmonBruh')


# sends a random Quote to the Twitch Chat
@bot.command(name='quote')
async def Quote(ctx):
    time = datetime.datetime.now().strftime('%H:%M:%S')
    try:
        quotes.load_quotes()
        await ctx.send(f'Quote #{quotes.quote_key}: {quotes.saved_quotes[quotes.quote_key]}')
        #print(f'{time} - [Twitch]  <Quote>: #{quotes.quote_key}: {quotes.saved_quotes[quotes.quote_key]}')

    except Exception as err:
        await ctx.send('In Moment gibt es keine Quotes NotLikeThis')


# removes a quote if a moderator or the channel owner
@bot.command(name='removequote')
async def RemoveQuote(ctx):
    viewer = ctx.author.name
    modlist = request.get_moderators()
    if viewer in modlist or viewer == CHANNEL_NAME:
        message = ctx.message.content
        _, quote_key = message.split(' ', 1)
        quotes.remove_quotes(quote_key)
        await ctx.send(f'{quotes.quote_removed}')
    else:
        await ctx.send(f'@{viewer} du hast keine berechtingung für diesen Befehl. cmonBruh')


# gives the time, how long the twitch channel is currently live
@bot.command(name='uptime')
async def Uptime(ctx):
    message = request.get_uptime(CHANNEL_NAME)
    await ctx.send(message)


# gives the time how long the follower is following
@bot.command(name='followage')
async def Followage(ctx):
    message = str(ctx.message.content).lower()
    viewer = str(ctx.author.name).lower()
    try:
        _, username = message.split(' ', 1)
        if username.startswith('@'):
            username = username[1:]
    except:
        username = viewer
    followage = request.followage(viewer, username)
    await ctx.send(f'{followage}')


# gives the time how long the follower is watching
@bot.command(name='watchtime')
async def Watchtime(ctx):
    message = ctx.message.content
    try:
        _, username = message.split(' ', 1)
        if str(username).startswith('@'):
            username = username[1:]
    except:
        username = ctx.author.name
    user_watchtime = watchtime.get_watchtime(username)

    if user_watchtime == None:
        await ctx.send(f'@{username} hat hier noch nicht zugeschaut. FailFish')
    else:
        await ctx.send(f'@{username} schaut seit {user_watchtime} zu!')


# sends the top 5 user and there watchtime to the twitch chat
@bot.command(name='topwatchtime', aliases=['tw'])
async def Top_Watchtime(ctx):
    top_5 = watchtime.get_watchtime_leaderboard()
    await ctx.send(top_5)


# counts up the crash count
@bot.command(name='silas')
async def Crash_count(ctx):
    filename = 'json/shared/crash_count.json'
    try:
        with open(filename, 'r') as save_file:
            crash_count = json.load(save_file)
        crash_count["crash_count"] += 1
        crash_count_message = crash_count['crash_count']
        await ctx.send(f'@SilasGC hat den Code schon {crash_count_message} mal gecrashed. louisd15Wah')
        with open(filename, 'w') as save_file:
            json.dump(crash_count, save_file, indent=4)
    except Exception as err:
        error = f'[Twitch Chatbot] Error in Crash_count: {err}'
        log.log_error(error)


# sends the crash count to the twitch chat
@bot.command(name='silascount')
async def Crash_count(ctx):
    filename = 'json/shared/crash_count.json'
    try:
        with open(filename, 'r') as save_file:
            crash_count = json.load(save_file)
        crash_count_message = crash_count['crash_count']
        await ctx.send(f'@SilasGC hat den Code schon {crash_count_message} mal gecrashed. louisd15Wah')
    except Exception as err:
        error = f'[Twitch Chatbot] Error in Crash_count: {err}'
        log.log_error(error)


# send a random number from 1 to the input number in the twitch chat 
@bot.command(name='rng')
async def Rgn(ctx):
    message = ctx.message.content
    try:
        _, number = message.split(' ', 1)
        number = int(number)
        random_number = random.randint(1, number)
        await ctx.send(f'@{ctx.author.name} es wurde die Zahl {random_number}.')
    except Exception as err:
        await ctx.send(f'@{ctx.author.name} der Befehl funktioniert so: !rng [max. Nummer]')
        error = f'[Twitch Chatbot] Error in Rgn: {err}'
        log.log_error(error)


# sends a message to the twitch chat, that one person hugged another
@bot.command(name='hug')
async def Hug(ctx):
    message = str(ctx.message.content).lower()
    author = str(ctx.author.name).lower()

    try:
        _, username = message.split(' ', 1)
        if username.startswith('@'):
            username = username[1:]
    
    except:
        await ctx.send(f'@{author} der Befehl geht so: !hug [@name]')
        return
    
    await ctx.send(f'{author} hat @{username} umarmt <3')
    return



# Minigames | minigames for the twitch chat like duel, gamble or stats leveling with currency
@bot.command(name='duel')
async def Duel(ctx):
    challenger = str(ctx.author.name).lower()
    message = str(ctx.message.content).lower()

    try:
        _, challenged = message.split(' ', 1)
        if challenged.startswith('@'):
            challenged = challenged[1:]
    except Exception as err:
        log.log_error(err)
        await ctx.send(f'@{challenger} der Befehl geht so: !duel [@Gegner] [bet]')
        return

    try:
        _, bet = challenged.split(' ', 1)
        if bet != '' or bet != ' ':
            try:
                bet = int(bet)
            except:
                await ctx.send(f'@{challenger} die Bet muss eine Zahl sein LUL')
                return
    except:
        bet = 0

    log.log_info(f'Challenger: {challenger}\nChallenged: {challenged}\nBet: {bet}')

    duel = minigame.Duel()

    answer, is_vaild = await duel.duel(int(bet), str(challenger), str(challenged))
    await ctx.send(answer)

    if not is_vaild:
        return

    answer = await duel.duel_is_valid()
    await ctx.send(answer)

@bot.command(name='accept')
async def Accept(ctx):
    challenged = str(ctx.author.name).lower()

    duel = minigame.Duel()
    answer = await duel.duel_accept(challenged)

    await ctx.send(answer)

@bot.command(name='deny')
async def Deny(ctx):
    challenged = str(ctx.author.name).lower()

    duel = minigame.Duel()
    answer = await duel.duel_deny(challenged)

    await ctx.send(answer)

@bot.command(name='exit')
async def Exit(ctx):
    challenger = str(ctx.author.name).lower()

    duel = minigame.Duel()
    answer = await duel.duel_exit(challenger)

    await ctx.send(answer)

@bot.command(name='balance', aliases=['stonks'])
async def Balance(ctx):
    message = str(ctx.message.content).lower()
    author = str(ctx.author.name).lower()
    try:
        _, username = message.split(' ', 1)
        if username.startswith('@'):
            username = str(username[1:])
    except:
        username = author

    answer = await minigame.Currency().get_balance(author, username)
    await ctx.send(answer)

@bot.command(name='topbalance', aliases=['tb'])
async def TopWatchtime(ctx):
    answer = await minigame.Currency().top_balance()
    await ctx.send(answer)

@bot.command(name='gamble')
async def Gamble(ctx):
    message = str(ctx.message.content)
    username = str(ctx.author.name)
    #log.log_info(f'in gamble message: {message}')
    try:
        _, bet = message.split(' ', 1)
        log.log_info(f'in gamble bet: {bet}')
    except:
        bet = 0

    answer = await minigame.Gamble().gamble(int(bet), str(username))
    await ctx.send(answer)

@bot.command(name='stats')
async def Stats(ctx):
    message = str(ctx.message.content).lower()
    author = str(ctx.author.name).lower()
    try:
        _, username = message.split(' ', 1)
        if username.startswith('@'):
            username = username[1:]
    except:
        username = author

    answer = minigame.Stats().get_stats(username)
    await ctx.send(answer)

@bot.command(name='rizz')
async def Rizz(ctx):
    username = str(ctx.author.name).lower()

    answer = minigame.Stats().buy_rizz(username)
    await ctx.send(answer)

@bot.command(name='sigma')
async def Sigma(ctx):
    username = str(ctx.author.name).lower()

    answer = minigame.Stats().buy_sigma(username)
    await ctx.send(answer)

@bot.command(name='aura')
async def Aura(ctx):
    username = str(ctx.author.name).lower()

    answer = minigame.Stats().buy_aura(username)
    await ctx.send(answer)



#Secrets Commands | Commands to check if the Bot still works
@bot.command(name='ping')
async def Ping(ctx):
    await ctx.send('pong')

@bot.command(name='pong')
async def Pong(ctx):
    await ctx.send('ping')

@bot.command(name='peng')
async def Peng(ctx):
    await ctx.send('pow')

@bot.command(name='pow')
async def Peng(ctx):
    await ctx.send('peng')



# Mod Commands | Commands that only moderator or the channel owner can use
# changes the title of the twitch stream
@bot.command(name='title')
async def Title(ctx):
    message = str(ctx.message.content)
    viewer = str(ctx.author.name)
    modlist = request.get_moderators()
    if viewer in modlist or viewer == CHANNEL_NAME:
        try:
            _, title = message.split(' ', 1)
            anwser = request.change_title(title)
            await ctx.send(f'{anwser}')
        except:
            await ctx.send(f'@{viewer} FailFish')
    else:
        await ctx.send(f'@{viewer} Du hast keine Berechtigung dafür.')


# change the game of the twitch stream
@bot.command(name='game')
async def Game(ctx):
    message = str(ctx.message.content)
    viewer = str(ctx.author.name)
    modlist = request.get_moderators()
    if viewer in modlist or viewer == CHANNEL_NAME:
        try:
            _, game = message.split(' ', 1)
            anwser = request.change_game(game)
            await ctx.send(f'{anwser}')
        except:
            await ctx.send(f'@{viewer} FailFish')
    else:
        await ctx.send(f'@{viewer} Du hast keine Berechtigung dafür.')



# Help Command | sends a list of commands to the twitch chat, that can be used
@bot.command(name='help', aliases=['command', 'commands', 'info', 'infos'])
async def Help(ctx):
    viewer = ctx.author.name
    command_list = [command.name for command in bot.commands.values()]
    block_command_list = ['ping', 'pong', 'peng', 'pow']
    message = f'@{viewer} hier sind die Befehle: ' + ', '.join(f'!{cmd}' for cmd in command_list if cmd not in block_command_list)
    await ctx.send(message)





# Start Stuff
def twitch_chatbot_start():
    bot.run()



if __name__ == '__main__':
    bot.run()