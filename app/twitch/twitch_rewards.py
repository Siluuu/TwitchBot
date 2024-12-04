import app.twitch.oauth_2 as oauth
import app.twitch.request as request
import app.twitch.tts as tts
import app.style.better_print as better_print
import app.logging as log
import os
import asyncio
import json
import websockets
import uuid
import random
import datetime
import re
from dotenv import load_dotenv
from rcon.source import Client

load_dotenv()

CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

CHANNEL_NAME = os.getenv('TWITCH_CHANNEL_NAME')
MC_USERNAME = 'Minecraft Username'

TWITCH_API_BASE_URL = 'https://api.twitch.tv/helix'
GET_USER_ID_URL = f'{TWITCH_API_BASE_URL}/users'
REDEMPTIONS_URL = f'{TWITCH_API_BASE_URL}/channel_points_custom_rewards/redemptions'

MC_SERVER_IP= os.getenv('MC_SERVER_IP')
MC_SERVER_PORT= os.getenv('MC_SERVER_PORT')
MC_SERVER_PW= os.getenv('MC_SERVER_PW')

REWARD_SPAWN_CREEPER= os.getenv('TWITCH_REWARD_SPAWN_CREEPER')
REWARD_SPAWN_ZOMBIE = os.getenv('TWITCH_REWARD_SPAWN_ZOMBIE')
REWARD_SPAWN_GROUP = os.getenv('TWITCH_REWARD_SPAWN_GROUP')
REWARD_EFFECT_BLINDNESS = os.getenv('TWITCH_REWARD_EFFECT_BLINDNESS')
REWARD_EFFECT_NAUSEA = os.getenv('TWITCH_REWARD_EFFECT_NAUSEA')
REWARD_EFFECT_SLOWNESS = os.getenv('TWITCH_REWARD_EFFECT_SLOWNESS')
REWARD_TP_RANDOM = os.getenv('TWITCH_REWARD_TP_RANDOM')
REWARD_TP_RANDOM_WORLD = os.getenv('TWITCH_REWARD_TP_RANDOM_WORLD')
REWARD_SOUND_CREEPER = os.getenv('TWITCH_REWARD_SOUND_CREEPER')
REWARD_GIVE_MAX = os.getenv('TWITCH_REWARD_GIVE_MAX')
REWARD_PICK_GAME = os.getenv('TWITCH_REWARD_PICK_GAME')
REWARD_DISCORD_ROLE = os.getenv('TWITCH_REWARD_DISCORD_ROLE')
REWARD_TTS = os.getenv('TWITCH_REWARD_TTS')



async def listen_to_channel_points():
    try:
        access_token = oauth.Oauth().get_last_tokens()

        nonce = str(uuid.uuid4())
        #user_id = 263974115
        user_id = request.fetch_user_id(CHANNEL_NAME)
        #print(f'User ID from {CHANNEL_NAME}: {user_id}')
        better_print.rewards_are_ready()
        while True:
            try:
                async with websockets.connect(f'wss://pubsub-edge.twitch.tv') as websocket:
                    await websocket.send(
                        json.dumps(
                            {
                                "type": "LISTEN",
                                "data": {
                                    "topics": [f"channel-points-channel-v1.{user_id}"],
                                    "auth_token": access_token,
                                },
                            }
                        )
                    )

                    while True:
                        response = await websocket.recv()
                        data = json.loads(response)

                        #reward_user = data['display_name']
                        #print(f'Received data: {data}')

                        if data.get('nonce') == nonce:
                            if data['type'] == 'RESPONSE' and data['error'] ==  '':
                                full_message = '[Twitch] Successfully subscribed to channel points.'
                                log.log_info(full_message)
                            else:
                                full_message = f'Error in response: ' + data['error']
                                if data['error'] == 'ERR_BADAUTH':
                                    access_token = oauth.Oauth().get_last_tokens()



                        try:
                            if data['type'] == 'MESSAGE':
                                message = json.loads(data['data']['message'])
                                #print(message)
                                reward_user = message['data']['redemption']['user']['display_name']
                                time = datetime.datetime.now().strftime('%H:%M:%S')
                                full_message = f'{time} - [Twitch] <Reward>: '+ message['data']['redemption']['reward']['title'] + f' eingelöst von {reward_user}'
                                log.log_info(full_message)


                                # Minecraft Rcon
                                if (message['data']['redemption']['reward']['title'] == REWARD_SPAWN_CREEPER):
                                    with Client(MC_SERVER_IP, int(MC_SERVER_PORT), passwd=MC_SERVER_PW) as client:
                                        response1 = client.run(str(f'execute at '+MC_USERNAME+' run summon minecraft:creeper ~ ~ ~ {CustomName:'+"'[{"+'"text":'+f'"{reward_user}"'+'}]'+"'}"))
                                        response2 = client.run(str('execute at '+MC_USERNAME+f' run playsound minecraft:block.note_block.chime ambient {MC_USERNAME}'))
                                    responses = f'{response1}, {response2}'
                                    log.log_info(response)


                                elif (message['data']['redemption']['reward']['title'] == REWARD_SPAWN_GROUP):
                                    with Client(MC_SERVER_IP, int(MC_SERVER_PORT), passwd=MC_SERVER_PW) as client:
                                        response1 = client.run(str('execute at '+MC_USERNAME+' run summon minecraft:zombie ~ ~ ~ {CustomName:'+"'[{"+'"text":'+f'"{reward_user}"'+'}]'+"'}"))
                                        response2 = client.run(str('execute at '+MC_USERNAME+' run summon minecraft:skeleton ~ ~ ~ {CustomName:'+"'[{"+'"text":'+f'"{reward_user}"'+'}]'+"'}"))
                                        response3 = client.run(str('execute at '+MC_USERNAME+' run summon minecraft:spider ~ ~ ~ {CustomName:'+"'[{"+'"text":'+f'"{reward_user}"'+'}]'+"'}"))
                                        response4 = client.run(str('execute at '+MC_USERNAME+f' run playsound minecraft:block.note_block.chime ambient {MC_USERNAME}'))
                                    responses = f'{response1}, {response2}, {response3}, {response4}'
                                    log.log_info(response)


                                elif (message['data']['redemption']['reward']['title'] == REWARD_EFFECT_BLINDNESS):
                                    with Client(MC_SERVER_IP, int(MC_SERVER_PORT), passwd=MC_SERVER_PW) as client:
                                        response = client.run(str(f'effect give {MC_USERNAME} minecraft:blindness 30 1'))
                                    responses = f'{response}'
                                    log.log_info(response)


                                elif (message['data']['redemption']['reward']['title'] == REWARD_EFFECT_NAUSEA):
                                    with Client(MC_SERVER_IP, int(MC_SERVER_PORT), passwd=MC_SERVER_PW) as client:
                                        response = client.run(str(f'effect give {MC_USERNAME} minecraft:nausea 30 1'))
                                    responses = f'{response}'
                                    log.log_info(response)


                                elif (message['data']['redemption']['reward']['title'] == REWARD_TP_RANDOM):
                                    with Client(MC_SERVER_IP, int(MC_SERVER_PORT), passwd=MC_SERVER_PW) as client:
                                        tp_max_range = 2000
                                        response1 = client.run(str(f'spreadplayers ~ ~ 1 {tp_max_range} false {MC_USERNAME}'))
                                    responses = f'{response1}'
                                    log.log_info(response)


                                elif (message['data']['redemption']['reward']['title'] == REWARD_SOUND_CREEPER):
                                    with Client(MC_SERVER_IP, int(MC_SERVER_PORT), passwd=MC_SERVER_PW) as client:
                                        response = client.run(str(f'execute at {MC_USERNAME} run playsound minecraft:entity.creeper.primed ambient {MC_USERNAME}'))
                                    responses = f'{response}'
                                    log.log_info(response)


                                elif (message['data']['redemption']['reward']['title'] == REWARD_GIVE_MAX):
                                    with Client(MC_SERVER_IP, int(MC_SERVER_PORT), passwd=MC_SERVER_PW) as client:

                                        random_inv = [
                                            f'minecraft:suspicious_stew 36 '+'{Effects:[{EffectId:19,EffectDuration:160}]}',
                                            f'minecraft:wooden_hoe 36 '+'{Damage:58}'
                                            ]

                                        random_inv = random.choice(random_inv)
                                        response = client.run(str(f'give {MC_USERNAME} {random_inv}'))
                                        responses = f'{response}'
                                        log.log_info(response)


                                elif (message['data']['redemption']['reward']['title'] == REWARD_TP_RANDOM_WORLD):
                                    with Client(MC_SERVER_IP, int(MC_SERVER_PORT), passwd=MC_SERVER_PW) as client:
                                        response1 = client.run(str(f'getlocation {MC_USERNAME}'))
                                        world_match = re.search(r'§6Current World:§c\s+(\w+)', response1)

                                        if world_match:
                                            current_world = world_match.group(1)
                                            if current_world == 'world':
                                                current_world = 'overworld'
                                            elif current_world == 'world_nether':
                                                current_world = 'the_nether'
                                            elif current_world == 'world_the_end':
                                                current_world = 'the_end'

                                        worlds = [
                                            'overworld',
                                            'overworld',
                                            'overworld',
                                            'overworld',
                                            'overworld',
                                            'overworld',
                                            'the_nether',
                                            'the_nether',
                                            'the_nether',
                                            'the_end'
                                            ]

                                        if current_world in worlds:
                                            while current_world in worlds:
                                                worlds.remove(current_world)

                                        random_world = random.choice(worlds)
                                        response2 = client.run(str(f'execute in minecraft:{random_world} run spreadplayers ~ ~ 1 1000 false {MC_USERNAME}'))
                                    responses = f'{response2}'
                                    log.log_info(response)


                                # Pick a Game
                                elif (message['data']['redemption']['reward']['title'] == REWARD_PICK_GAME):
                                    
                                    redemption_id = message['data']['redemption']['id']
                                    reward_id = message['data']['redemption']['reward']['id']
                                    new_game = message['data']['redemption']['user_input']
                                    filename = 'json/twitch/pick_game.json'
                                    pick_game_dict = {}
                                    game_list = []

                                    with open(filename, 'r') as load_file:
                                        pick_game_dict = json.load(load_file)
                                        requested_games = pick_game_dict.get('requested_games', {})
                                        played_games = pick_game_dict.get('played_games', {})

                                    if requested_games != {}:
                                        for key in requested_games:
                                            game = requested_games[key]
                                            game = str(game).replace(' ', '').lower()
                                            game_list.append(game)

                                    if played_games != {}:
                                        for key in played_games:
                                            game = played_games[key]
                                            game = str(game).replace(' ', '').lower()
                                            game_list.append(game)

                                        
                                    #log.log_info(f'New Game: {new_game}\nGame List: {game_list}')

                                    if str(new_game).replace(' ', '').lower() in game_list:
                                        status = 'canceled'
                                        
                                    else:
                                        next_key = str(max(map(int, pick_game_dict['requested_games'].keys()), default=0) + 1)
                                        pick_game_dict['requested_games'][next_key] = new_game

                                        with open(filename, 'w') as save_file:
                                            json.dump(pick_game_dict, save_file, indent=4)

                                        status = 'fulfilled'

                                    request.update_redemption_status(redemption_id, reward_id, status)

                                    log.log_info(f'Pick a game!: {new_game}')


                                # Discord Role
                                elif (message['data']['redemption']['reward']['title'] == f'{REWARD_DISCORD_ROLE}'):
                                    dc_name = str(message['data']['redemption']['user_input']).lower()
                                    twitch_name = str(reward_user).lower()

                                    twitch_mod_list = request.get_moderators()
                                    twitch_vip_list = request.get_vips()
                                    twitch_sub_list = request.get_broadcaster_supcriptions()

                                    if twitch_name in twitch_mod_list or twitch_name in twitch_vip_list or twitch_name in twitch_sub_list:
                                        filename = 'json/discord/request_verification.json'
                                        with open(filename, 'r') as request_file:
                                            request_user = json.load(request_file)

                                        request_user[f'{twitch_name}'] = f'{dc_name}'

                                        with open(filename, 'w') as request_file:
                                            request_user = json.dump(request_user, request_file, indent=4)

                                # TTS
                                elif (message['data']['redemption']['reward']['title'] == f'{REWARD_TTS}'):
                                    tts_text = str(message['data']['redemption']['user_input']).lower()
                                    username = str(reward_user).lower()
                                    #tts.tts_2(tts_text, username)


                                elif (message['data']['redemption']['reward']['title'] == 'placeholder'):
                                   pass
                        except Exception as err:
                            error = f'[Twitch Rewards] Error in data: {err}'
                            log.log_error(error)
            except Exception as err:
                error = f'[Twitch Rewards] Error in websocket: {err}'
                log.log_error(error)
    except Exception as err:
        error = f'[Twitch Rewards] Error in listen_to_channel_points: {err}'
        log.log_error(error)


def twitch_rewards_start():
    asyncio.run(listen_to_channel_points())

if __name__ == '__main__':
    twitch_rewards_start()
